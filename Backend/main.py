import uuid
from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import schemas
import analytics_service
from firebase_service import get_current_user, db, bucket, use_mock

app = FastAPI(
    title="Online Hobby & Skills Tracker API",
    version="1.0.0",
    description="Industry-standard Cloud Computing Backend with FastAPI and Firebase"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store fallback when operating in local student simulation mode
local_db = {
    "users": {},
    "skills": {},
    "goals": {},
    "practice": [],
    "posts": {},
    "comments": [],
    "likes": set() # tuple: (post_id, user_id)
}

@app.get("/healthz", tags=["System"])
def health_check():
    return {"status": "healthy", "cloud_connected": db is not None, "timestamp": datetime.utcnow().isoformat()}

# --- PROFILE MODULE ---
@app.get("/api/profile", tags=["Profile"])
def get_profile(user: dict = Depends(get_current_user)):
    uid = user["uid"]
    if db is not None:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            return doc.to_dict()
    return local_db["users"].get(uid, {"user_id": uid, "name": user.get("name", "Student User"), "email": user.get("email")})

@app.put("/api/profile", tags=["Profile"])
def update_profile(data: schemas.UserProfileUpdate, user: dict = Depends(get_current_user)):
    uid = user["uid"]
    profile_data = {k: v for k, v in data.model_dump().items() if v is not None}
    profile_data.update({"user_id": uid, "updated_at": datetime.utcnow().isoformat()})
    
    if db is not None:
        db.collection("users").document(uid).set(profile_data, merge=True)
    else:
        current = local_db["users"].get(uid, {})
        current.update(profile_data)
        local_db["users"][uid] = current
        
    return {"message": "Profile updated successfully", "profile": profile_data}

# --- SKILLS MODULE ---
@app.post("/api/skills", status_code=status.HTTP_201_CREATED, tags=["Skills"])
def create_skill(skill: schemas.SkillCreate, user: dict = Depends(get_current_user)):
    skill_id = str(uuid.uuid4())
    record = skill.model_dump()
    record.update({
        "skill_id": skill_id,
        "user_id": user["uid"],
        "status": "ACTIVE",
        "created_at": datetime.utcnow().isoformat()
    })
    if db is not None:
        db.collection("skills").document(skill_id).set(record)
    else:
        local_db["skills"][skill_id] = record
    return record

@app.get("/api/skills", tags=["Skills"])
def get_my_skills(user: dict = Depends(get_current_user)):
    uid = user["uid"]
    if db is not None:
        docs = db.collection("skills").where("user_id", "==", uid).stream()
        return [d.to_dict() for d in docs]
    return [s for s in local_db["skills"].values() if s["user_id"] == uid]

# --- GOALS MODULE ---
@app.post("/api/goals", status_code=status.HTTP_201_CREATED, tags=["Goals"])
def create_goal(goal: schemas.GoalCreate, user: dict = Depends(get_current_user)):
    goal_id = str(uuid.uuid4())
    record = goal.model_dump()
    record.update({
        "goal_id": goal_id,
        "user_id": user["uid"],
        "current_value": 0.0,
        "progress_percentage": 0.0,
        "status": "IN_PROGRESS",
        "created_at": datetime.utcnow().isoformat()
    })
    if db is not None:
        db.collection("goals").document(goal_id).set(record)
    else:
        local_db["goals"][goal_id] = record
    return record

# --- PRACTICE SESSION & STREAK MODULE ---
@app.post("/api/practice", status_code=status.HTTP_201_CREATED, tags=["Practice"])
def log_practice(practice: schemas.PracticeCreate, user: dict = Depends(get_current_user)):
    session_id = str(uuid.uuid4())
    record = practice.model_dump()
    practiced_date = record.get("practiced_at") or date.today()
    record["practiced_at"] = str(practiced_date)
    record.update({
        "session_id": session_id,
        "user_id": user["uid"],
        "created_at": datetime.utcnow().isoformat()
    })

    added_hours = round(record["duration_minutes"] / 60.0, 2)

    # 1. Save practice log
    if db is not None:
        db.collection("practice").document(session_id).set(record)
        # Update matching goals for this skill
        goals = db.collection("goals").where("user_id", "==", user["uid"]).where("skill_id", "==", record["skill_id"]).stream()
        for g in goals:
            g_data = g.to_dict()
            new_curr = round(g_data.get("current_value", 0.0) + added_hours, 2)
            prog = analytics_service.calculate_goal_progress(g_data["target_value"], new_curr)
            db.collection("goals").document(g.id).update({
                "current_value": new_curr,
                "progress_percentage": prog["progress_percentage"],
                "status": prog["status"]
            })
    else:
        local_db["practice"].append(record)
        for g in local_db["goals"].values():
            if g["user_id"] == user["uid"] and g["skill_id"] == record["skill_id"]:
                g["current_value"] = round(g.get("current_value", 0.0) + added_hours, 2)
                prog = analytics_service.calculate_goal_progress(g["target_value"], g["current_value"])
                g["progress_percentage"] = prog["progress_percentage"]
                g["status"] = prog["status"]

    return {"message": "Practice logged successfully", "session": record}

# --- COMMUNITY FEED & POSTS ---
@app.post("/api/posts", status_code=status.HTTP_201_CREATED, tags=["Community"])
def create_post(post: schemas.PostCreate, user: dict = Depends(get_current_user)):
    post_id = str(uuid.uuid4())
    record = post.model_dump()
    record.update({
        "post_id": post_id,
        "user_id": user["uid"],
        "author_name": user.get("name", "Student Member"),
        "likes_count": 0,
        "comments_count": 0,
        "created_at": datetime.utcnow().isoformat()
    })
    if db is not None:
        db.collection("posts").document(post_id).set(record)
    else:
        local_db["posts"][post_id] = record
    return record

@app.get("/api/feed", tags=["Community"])
def get_community_feed():
    if db is not None:
        docs = db.collection("posts").order_by("created_at", direction=firestore.Query.DESCENDING).limit(50).stream()
        return [d.to_dict() for d in docs]
    return sorted(local_db["posts"].values(), key=lambda x: x["created_at"], reverse=True)

# --- SOCIAL INTERACTIONS: LIKES & COMMENTS ---
@app.post("/api/posts/{post_id}/like", tags=["Community"])
def like_post(post_id: str, user: dict = Depends(get_current_user)):
    pair = (post_id, user["uid"])
    if pair in local_db["likes"]:
        raise HTTPException(status_code=400, detail="You already liked this post.")
    local_db["likes"].add(pair)
    if post_id in local_db["posts"]:
        local_db["posts"][post_id]["likes_count"] += 1
    return {"message": "Post liked successfully"}

@app.delete("/api/posts/{post_id}/like", tags=["Community"])
def unlike_post(post_id: str, user: dict = Depends(get_current_user)):
    pair = (post_id, user["uid"])
    if pair not in local_db["likes"]:
        raise HTTPException(status_code=404, detail="Like not found.")
    local_db["likes"].remove(pair)
    if post_id in local_db["posts"]:
        local_db["posts"][post_id]["likes_count"] = max(0, local_db["posts"][post_id]["likes_count"] - 1)
    return {"message": "Post unliked successfully"}

@app.post("/api/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED, tags=["Community"])
def add_comment(post_id: str, comment: schemas.CommentCreate, user: dict = Depends(get_current_user)):
    comment_id = str(uuid.uuid4())
    record = comment.model_dump()
    record.update({
        "comment_id": comment_id,
        "post_id": post_id,
        "user_id": user["uid"],
        "author_name": user.get("name", "Student Member"),
        "created_at": datetime.utcnow().isoformat()
    })
    local_db["comments"].append(record)
    if post_id in local_db["posts"]:
        local_db["posts"][post_id]["comments_count"] += 1
    return record

# --- ANALYTICS DASHBOARD ---
@app.get("/api/analytics/dashboard", tags=["Analytics"])
def get_user_dashboard(user: dict = Depends(get_current_user)):
    uid = user["uid"]
    user_sessions = [p for p in local_db["practice"] if p["user_id"] == uid]
    total_minutes = sum(p["duration_minutes"] for p in user_sessions)
    session_dates = [datetime.fromisoformat(p["created_at"]).date() for p in user_sessions]
    streaks = analytics_service.calculate_practice_streaks(session_dates)
    
    my_goals = [g for g in local_db["goals"].values() if g["user_id"] == uid]
    completed_goals = sum(1 for g in my_goals if g["status"] == "COMPLETED")

    return {
        "total_practice_hours": round(total_minutes / 60.0, 1),
        "total_sessions": len(user_sessions),
        "current_streak_days": streaks["current_streak"],
        "longest_streak_days": streaks["longest_streak"],
        "active_goals": len(my_goals) - completed_goals,
        "completed_goals": completed_goals
    }
