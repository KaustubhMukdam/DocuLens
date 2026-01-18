"""Discussion model."""

from uuid import UUID

from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import GUID

from app.models.base import Base


class Discussion(Base):
    """Discussion model."""
    
    __tablename__ = "discussions"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("doc_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    user_id: Mapped[UUID] = mapped_column(
        GUID(),
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
