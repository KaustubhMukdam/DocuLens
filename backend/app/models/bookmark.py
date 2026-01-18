"""Bookmark model."""

from typing import Optional
from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import GUID

from app.models.base import Base


class Bookmark(Base):
    """Bookmark model."""
    
    __tablename__ = "bookmarks"
    
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
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="bookmarks")
