"""
User model for authentication and user management.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base


class SkillLevel(str, enum.Enum):
    """User skill level enum."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    # Basic info
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    
    # Learning preferences
    skill_level: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel),
        default=SkillLevel.BEGINNER,
        nullable=False
    )
    
    preferred_language: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Account status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # OAuth fields
    google_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )
    
    github_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )
    
    # Relationships
    learning_paths: Mapped[list["LearningPath"]] = relationship(
        "LearningPath",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    progress: Mapped[list["UserProgress"]] = relationship(
        "UserProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    bookmarks: Mapped[list["Bookmark"]] = relationship(
        "Bookmark",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    notes: Mapped[list["UserNote"]] = relationship(
        "UserNote",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    discussions: Mapped[list["Discussion"]] = relationship(
        "Discussion",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    comments: Mapped[list["DiscussionComment"]] = relationship(
        "DiscussionComment",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"