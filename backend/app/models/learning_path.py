"""Learning path model."""

from typing import Optional, TYPE_CHECKING
from uuid import UUID
from datetime import datetime
import enum

from sqlalchemy import String, Enum as SQLEnum, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.language import Language


class PathType(str, enum.Enum):
    """Learning path type."""
    QUICK = "quick"
    DEEP = "deep"


class PathStatus(str, enum.Enum):
    """Learning path status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LearningPath(Base):
    """Learning path model."""
    
    __tablename__ = "learning_paths"
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    language_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("languages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    path_type: Mapped[PathType] = mapped_column(
        SQLEnum(PathType),
        nullable=False
    )
    
    status: Mapped[PathStatus] = mapped_column(
        SQLEnum(PathStatus),
        default=PathStatus.NOT_STARTED,
        nullable=False
    )
    
    progress_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0.00,
        nullable=False
    )
    
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships with string references to avoid circular imports
    user: Mapped["User"] = relationship("User", back_populates="learning_paths")
    language: Mapped["Language"] = relationship("Language", back_populates="learning_paths")