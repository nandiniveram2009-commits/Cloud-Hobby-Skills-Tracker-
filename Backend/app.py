from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

app = FastAPI(
    title="Cloud Hobby & Skills Tracker API",
    version="1.0.0",
    description="Backend API for tracking skills, practice sessions, goals, and community sharing."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Mock Database for Local Demonstration
# (In production, replace with Cloud Firestore or PostgreSQL connection pool)
fake_users_db = {}
fake_skills_db = {}
fake_practice_db = {}
fake_posts_db = {}
fake_likes_db = set()
fake_comments_db = []

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class SkillCreate(BaseModel):
    user_id: str
    skill_name: str
    category: str
    current_level: str
    target_level: str
    description: Optional[str] = ""

class PracticeCreate(BaseModel):
    user_id: str
    skill_id: str
    duration_minutes: int
    activity: str
    notes: Optional[str] = ""

class PostCreate(BaseModel):
    user_id: str
    skill_id: Optional[str] = None
    content: str
    media_url: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "service": "Cloud Hobby & Skills Tracker API"}

@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user_{len(fake_users_db) + 1}"
    fake_users_db[user.email] = {
        "user_id": user_id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    return {"message": "User registered successfully", "user_id": user_id}

@app.post("/api/skills", status_code=status.HTTP_201_CREATED)
def create_skill(skill: SkillCreate):
    skill_id = f"skill_{len(fake_skills_db) + 1}"
    skill_data = skill.dict()
    skill_data["skill_id"] = skill_id
    skill_data["created_at"] = datetime.datetime.utcnow().isoformat()
    fake_skills_db[skill_id] = skill_data
    return {"message": "Skill created successfully", "skill_id": skill_id}

@app.get("/api/skills/{user_id}")
def get_user_skills(user_id: str):
    user_skills = [s for s in fake_skills_db.values() if s["user_id"] == user_id]
    return {"skills": user_skills}

@app.post("/api/practice", status_code=status.HTTP_201_CREATED)
def log_practice(practice: PracticeCreate):
    session_id = f"session_{len(fake_practice_db) + 1}"
    session_data = practice.dict()
    session_data["session_id"] = session_id
    session_data["practiced_at"] = datetime.datetime.utcnow().isoformat()
    fake_practice_db[session_id] = session_data
    return {"message": "Practice session logged successfully", "session_id": session_id}

@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    post_id = f"post_{len(fake_posts_db) + 1}"
    post_data = post.dict()
    post_data["post_id"] = post_id
    post_data["created_at"] = datetime.datetime.utcnow().isoformat()
    fake_posts_db[post_id] = post_data
    return {"message": "Community post created successfully", "post_id": post_id}

@app.get("/api/feed")
def get_community_feed():
    posts = list(fake_posts_db.values())
    posts.sort(key=lambda x: x["created_at"], reverse=True)
    return {"feed": posts}

@app.get("/api/analytics/{user_id}")
def get_user_analytics(user_id: str):
    user_sessions = [s for s in fake_practice_db.values() if s["user_id"] == user_id]
    total_minutes = sum(s["duration_minutes"] for s in user_sessions)
    total_skills = len([s for s in fake_skills_db.values() if s["user_id"] == user_id])
    
    return {
        "user_id": user_id,
        "total_practice_hours": round(total_minutes / 60.0, 2),
        "total_sessions": len(user_sessions),
        "active_skills": total_skills,
        "current_streak": 5 # Mock calculated streak
}
