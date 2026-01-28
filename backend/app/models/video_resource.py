"""Video resource model."""

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import GUID
from app.models.base import Base


class VideoResource(Base):
    """Video resource model."""
    
    __tablename__ = "video_resources"
    
    doc_section_id: Mapped[UUID] = mapped_column(
        GUID(),
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
    
    # ADD THIS FIELD - Required by scraper
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # FIX: Use Mapped instead of Column for consistency and make non-nullable with default
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    @property
    def url(self) -> str:
        """Alias for video_url to match API response schema."""
        return self.video_url  # FIXED: Was self.youtube_url (which doesn't exist)
    
    doc_section: Mapped["DocSection"] = relationship(
        "DocSection",
        back_populates="video_resources"
    )