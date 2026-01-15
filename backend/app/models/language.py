"""
Programming Language model.
"""

from typing import Optional
from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Language(Base):
    """Programming language/framework model."""
    
    __tablename__ = "languages"
    
    # Basic info
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    
    official_doc_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    logo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    version: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )
    
    # Metadata
    last_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )
    
    # Relationships
    doc_sections: Mapped[list["DocSection"]] = relationship(
        "DocSection",
        back_populates="language",
        cascade="all, delete-orphan"
    )
    
    learning_paths: Mapped[list["LearningPath"]] = relationship(
        "LearningPath",
        back_populates="language",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Language(id={self.id}, name={self.name}, slug={self.slug})>"