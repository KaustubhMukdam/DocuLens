"""Practice problem model."""

from typing import Optional
from uuid import UUID
import enum

from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey, ARRAY
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
    platform: Mapped[ProblemPlatform] = mapped_column(SQLEnum(ProblemPlatform), nullable=False)
    problem_url: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[ProblemDifficulty] = mapped_column(SQLEnum(ProblemDifficulty), nullable=False)
    topics: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="practice_problems"
    )
