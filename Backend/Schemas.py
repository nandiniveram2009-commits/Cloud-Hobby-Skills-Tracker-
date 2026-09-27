from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    interests: Optional[List[str]] = []

class SkillCreate(BaseModel):
    skill_name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., description="Music, Coding, Art, Fitness, Language, Other")
    current_level: str = Field("BEGINNER", pattern="^(BEGINNER|INTERMEDIATE|ADVANCED)$")
    target_level: str = Field("ADVANCED", pattern="^(BEGINNER|INTERMEDIATE|ADVANCED)$")
    description: Optional[str] = None

class GoalCreate(BaseModel):
    skill_id: str
    title: str
    target_value: float = Field(..., gt=0, description="Target hours or units")
    deadline: Optional[date] = None

class PracticeSessionCreate(BaseModel):
    skill_id: str
    duration_minutes: int = Field(..., gt=0, description="Practice duration in minutes")
    activity: str
    notes: Optional[str] = None
    practiced_at: Optional[date] = None

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    skill_id: Optional[str] = None
    media_url: Optional[str] = None

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
