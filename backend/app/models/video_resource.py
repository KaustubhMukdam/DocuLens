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
