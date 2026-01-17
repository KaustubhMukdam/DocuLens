"""
User schemas for request/response.
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    skill_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    preferred_language: Optional[str] = Field(None, max_length=50)


class UserResponse(BaseModel):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    skill_level: str
    preferred_language: Optional[str]
    is_active: bool
    is_premium: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class UserProfileResponse(UserResponse):
    """Extended user profile response with statistics."""
    total_learning_paths: int = 0
    completed_paths: int = 0
    total_sections_completed: int = 0
    total_time_spent_minutes: int = 0
    current_streak_days: int = 0