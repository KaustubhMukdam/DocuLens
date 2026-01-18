"""User progress model."""

from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import Boolean, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import GUID

from app.models.base import Base


class UserProgress(Base):
    """User progress tracking model."""
    
    __tablename__ = "user_progress"
    
    user_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    doc_section_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="progress")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="user_progress")
