# ============================================================================
# app/crud/video_resource.py
# ============================================================================
"""Video resource CRUD operations."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video_resource import VideoResource
from app.crud.base import CRUDBase
from pydantic import BaseModel


class VideoResourceCreate(BaseModel):
    """Schema for creating video resource."""
    doc_section_id: UUID
    title: str
    url: str
    platform: str = "youtube"
    duration_seconds: Optional[int] = None
    channel_name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0


class VideoResourceUpdate(BaseModel):
    """Schema for updating video resource."""
    title: Optional[str] = None
    url: Optional[str] = None
    duration_seconds: Optional[int] = None
    channel_name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None


class CRUDVideoResource(CRUDBase[VideoResource, VideoResourceCreate, VideoResourceUpdate]):
    """CRUD operations for VideoResource model."""
    
    async def get_by_section(
        self,
        db: AsyncSession,
        *,
        section_id: UUID
    ) -> List[VideoResource]:
        """Get all video resources for a section."""
        result = await db.execute(
            select(VideoResource)
            .where(VideoResource.doc_section_id == section_id)
            .order_by(VideoResource.order_index)
        )
        return list(result.scalars().all())
    
    async def get_by_language(
        self,
        db: AsyncSession,
        *,
        language_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[VideoResource]:
        """Get all video resources for a language."""
        from app.models.doc_section import DocSection
        
        result = await db.execute(
            select(VideoResource)
            .join(DocSection)
            .where(DocSection.language_id == language_id)
            .order_by(desc(VideoResource.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


# Global instance
video_resource_crud = CRUDVideoResource(VideoResource)
