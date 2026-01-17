"""
Documentation section model.
"""

from typing import Optional
from uuid import UUID
import enum

from sqlalchemy import String, Text, Integer, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class Difficulty(str, enum.Enum):
    """Section difficulty level."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class DocSection(Base):
    """Documentation section model."""
    
    __tablename__ = "doc_sections"
    
    # Foreign Keys
    language_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("languages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    parent_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    # Content
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )
    
    content_raw: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    content_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    # Ordering and metadata
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    
    estimated_time_minutes: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    
    difficulty: Mapped[Difficulty] = mapped_column(
        SQLEnum(Difficulty),
        default=Difficulty.MEDIUM,
        nullable=False
    )
    
    # Learning path flags
    is_quick_path: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )
    
    is_deep_path: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    # Relationships
    language: Mapped["Language"] = relationship(
        "Language",
        back_populates="doc_sections"
    )
    
    parent: Mapped[Optional["DocSection"]] = relationship(
        "DocSection",
        remote_side="DocSection.id",
        back_populates="children"
    )
    
    children: Mapped[list["DocSection"]] = relationship(
        "DocSection",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    
    code_examples: Mapped[list["CodeExample"]] = relationship(
        "CodeExample",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    practice_problems: Mapped[list["PracticeProblem"]] = relationship(
        "PracticeProblem",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    video_resources: Mapped[list["VideoResource"]] = relationship(
        "VideoResource",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    user_progress: Mapped[list["UserProgress"]] = relationship(
        "UserProgress",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    bookmarks: Mapped[list["Bookmark"]] = relationship(
        "Bookmark",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    notes: Mapped[list["UserNote"]] = relationship(
        "UserNote",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    discussions: Mapped[list["Discussion"]] = relationship(
        "Discussion",
        back_populates="doc_section",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<DocSection(id={self.id}, title={self.title}, slug={self.slug})>"