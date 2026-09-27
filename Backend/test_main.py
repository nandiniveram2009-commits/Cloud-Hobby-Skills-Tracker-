import pytest
from fastapi.testclient import TestClient
from main import app, local_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database():
    local_db["users"].clear()
    local_db["skills"].clear()
    local_db["goals"].clear()
    local_db["practice"].clear()
    local_db["posts"].clear()
    local_db["comments"].clear()
    local_db["likes"].clear()

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_skill_and_goal():
    headers = {"Authorization": "Bearer mock-token-user-a"}
    
    # 1. Create Skill
    skill_res = client.post("/api/skills", json={
        "skill_name": "Classical Guitar",
        "category": "Music",
        "current_level": "BEGINNER",
        "target_level": "INTERMEDIATE"
    }, headers=headers)
    assert skill_res.status_code == 201
    skill_id = skill_res.json()["skill_id"]

    # 2. Create Goal
    goal_res = client.post("/api/goals", json={
        "skill_id": skill_id,
        "title": "Master Fingerpicking (10 Hours)",
        "target_value": 10.0
    }, headers=headers)
    assert goal_res.status_code == 201
    assert goal_res.json()["target_value"] == 10.0

def test_practice_logging_updates_goal_progress():
    headers = {"Authorization": "Bearer mock-token-user-a"}
    
    # Setup
    s = client.post("/api/skills", json={"skill_name": "Painting", "category": "Art"}, headers=headers).json()
    client.post("/api/goals", json={"skill_id": s["skill_id"], "title": "Paint 10 hrs", "target_value": 10.0}, headers=headers)
    
    # Log 120 minutes (2 hours)
    res = client.post("/api/practice", json={
        "skill_id": s["skill_id"],
        "duration_minutes": 120,
        "activity": "Watercolors study"
    }, headers=headers)
    assert res.status_code == 201

    # Verify Analytics
    stats = client.get("/api/analytics/dashboard", headers=headers).json()
    assert stats["total_practice_hours"] == 2.0
    assert stats["current_streak_days"] == 1

def test_prevent_duplicate_likes():
    headers_a = {"Authorization": "Bearer mock-token-user-a"}
    
    # User A creates post
    post = client.post("/api/posts", json={"content": "Achieved 10-day streak! 🎸"}, headers=headers_a).json()
    post_id = post["post_id"]

    # Like once
    res1 = client.post(f"/api/posts/{post_id}/like", headers=headers_a)
    assert res1.status_code == 200

    # Like twice -> Expected 400 Bad Request
    res2 = client.post(f"/api/posts/{post_id}/like", headers=headers_a)
    assert res2.status_code == 400
    assert "already liked" in res2.json()["detail"]
