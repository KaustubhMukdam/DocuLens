"""Practice problem model."""

from typing import Optional
from uuid import UUID
import enum

from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, GUID, StringArray  # Import StringArray


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
        GUID(),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[ProblemPlatform] = mapped_column(SQLEnum(ProblemPlatform), nullable=False)
    problem_url: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[ProblemDifficulty] = mapped_column(SQLEnum(ProblemDifficulty), nullable=False)
    
    # Changed: Use StringArray instead of ARRAY(String)
    topics: Mapped[Optional[list[str]]] = mapped_column(StringArray(), nullable=True)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="practice_problems"
    )