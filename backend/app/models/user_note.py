"""User note model."""

from uuid import UUID

from sqlalchemy import Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import GUID

from app.models.base import Base


class UserNote(Base):
    """User note model."""
    
    __tablename__ = "user_notes"
    
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
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship("User", back_populates="notes")
    doc_section: Mapped["DocSection"] = relationship("DocSection", back_populates="notes")
