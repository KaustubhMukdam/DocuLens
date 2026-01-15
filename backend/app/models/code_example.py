# ============================================================================
# app/models/code_example.py
# ============================================================================
"""Code example model."""

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class CodeExample(Base):
    """Code example model."""
    
    __tablename__ = "code_examples"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_runnable: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="code_examples"
    )


# ============================================================================
# app/models/learning_path.py
# ============================================================================
"""Learning path model."""

from typing import Optional
from uuid import UUID
from datetime import datetime
import enum

from sqlalchemy import String, Enum, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


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
        Enum(PathType),
        nullable=False
    )
    
    status: Mapped[PathStatus] = mapped_column(
        Enum(PathStatus),
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
    
    user: Mapped["User"] = relationship("User", back_populates="learning_paths")
    language: Mapped["Language"] = relationship("Language", back_populates="learning_paths")


# ============================================================================
# app/models/user_progress.py
# ============================================================================
"""User progress model."""

from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import Boolean, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class UserProgress(Base):
    """User progress tracking model."""
    
    __tablename__ = "user_progress"
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
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


# ============================================================================
# app/models/practice_problem.py
# ============================================================================
"""Practice problem model."""

from typing import Optional
from uuid import UUID
import enum

from sqlalchemy import String, Text, Enum, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class ProblemPlatform(str, enum.Enum):
    """Problem platform."""
    LEETCODE = "leetcode"
    HACKERRANK = "hackerrank"
    CODEWARS = "codewars"
    EXERCISM = "exercism"


class ProblemDifficulty(str, enum.Enum):
    """Problem difficulty."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class PracticeProblem(Base):
    """Practice problem model."""
    
    __tablename__ = "practice_problems"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[ProblemPlatform] = mapped_column(Enum(ProblemPlatform), nullable=False)
    problem_url: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[ProblemDifficulty] = mapped_column(Enum(ProblemDifficulty), nullable=False)
    topics: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="practice_problems"
    )


# ============================================================================
# app/models/video_resource.py
# ============================================================================
"""Video resource model."""

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class VideoResource(Base):
    """Video resource model."""
    
    __tablename__ = "video_resources"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), default="youtube")
    video_url: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    views: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="video_resources"
    )


# ============================================================================
# app/models/bookmark.py
# ============================================================================
"""Bookmark model."""

from typing import Optional
from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class Bookmark(Base):
    """Bookmark model."""
    
    __tablename__ = "bookmarks"
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="bookmarks")


# ============================================================================
# app/models/user_note.py
# ============================================================================
"""User note model."""

from uuid import UUID

from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class UserNote(Base):
    """User note model."""
    
    __tablename__ = "user_notes"
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship("User", back_populates="notes")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="notes")


# ============================================================================
# app/models/discussion.py
# ============================================================================
"""Discussion model."""

from uuid import UUID

from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class Discussion(Base):
    """Discussion model."""
    
    __tablename__ = "discussions"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    is_solved: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship("User", back_populates="discussions")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="discussions")
    
    comments: Mapped[list["DiscussionComment"]] = relationship(
        "DiscussionComment",
        back_populates="discussion",
        cascade="all, delete-orphan"
    )


# ============================================================================
# app/models/discussion_comment.py
# ============================================================================
"""Discussion comment model."""

from uuid import UUID

from sqlalchemy import Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class DiscussionComment(Base):
    """Discussion comment model."""
    
    __tablename__ = "discussion_comments"
    
    discussion_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("discussions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0)
    is_solution: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship("User", back_populates="comments")
    discussion: Mapped["Discussion"] = relationship("Discussion", back_populates="comments")