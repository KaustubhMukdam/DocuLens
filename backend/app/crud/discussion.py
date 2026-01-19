# ============================================================================
# app/crud/discussion.py
# ============================================================================
"""Discussion CRUD operations."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.discussion import Discussion
from app.models.discussion_comment import DiscussionComment
from app.crud.base import CRUDBase
from pydantic import BaseModel


class DiscussionCreate(BaseModel):
    """Schema for creating discussion."""
    doc_section_id: UUID
    title: str
    content: str


class DiscussionUpdate(BaseModel):
    """Schema for updating discussion."""
    title: Optional[str] = None
    content: Optional[str] = None
    is_resolved: Optional[bool] = None


class CommentCreate(BaseModel):
    """Schema for creating comment."""
    discussion_id: UUID
    content: str
    parent_comment_id: Optional[UUID] = None


class CommentUpdate(BaseModel):
    """Schema for updating comment."""
    content: Optional[str] = None


class CRUDDiscussion(CRUDBase[Discussion, DiscussionCreate, DiscussionUpdate]):
    """CRUD operations for Discussion model."""
    
    async def get_by_section(
        self,
        db: AsyncSession,
        *,
        section_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Discussion]:
        """Get discussions for a section."""
        result = await db.execute(
            select(Discussion)
            .where(Discussion.doc_section_id == section_id)
            .options(selectinload(Discussion.user))
            .order_by(desc(Discussion.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Discussion]:
        """Get discussions created by user."""
        result = await db.execute(
            select(Discussion)
            .where(Discussion.user_id == user_id)
            .options(selectinload(Discussion.doc_section))
            .order_by(desc(Discussion.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_with_comments(
        self,
        db: AsyncSession,
        *,
        discussion_id: UUID
    ) -> Optional[Discussion]:
        """Get discussion with all comments."""
        result = await db.execute(
            select(Discussion)
            .where(Discussion.id == discussion_id)
            .options(
                selectinload(Discussion.user),
                selectinload(Discussion.comments).selectinload(DiscussionComment.user)
            )
        )
        return result.scalar_one_or_none()
    
    async def count_by_section(
        self,
        db: AsyncSession,
        *,
        section_id: UUID
    ) -> int:
        """Count discussions for a section."""
        result = await db.execute(
            select(func.count())
            .select_from(Discussion)
            .where(Discussion.doc_section_id == section_id)
        )
        return result.scalar_one()


class CRUDComment(CRUDBase[DiscussionComment, CommentCreate, CommentUpdate]):
    """CRUD operations for DiscussionComment model."""
    
    async def get_by_discussion(
        self,
        db: AsyncSession,
        *,
        discussion_id: UUID
    ) -> List[DiscussionComment]:
        """Get all comments for a discussion."""
        result = await db.execute(
            select(DiscussionComment)
            .where(DiscussionComment.discussion_id == discussion_id)
            .options(selectinload(DiscussionComment.user))
            .order_by(DiscussionComment.created_at)
        )
        return list(result.scalars().all())
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[DiscussionComment]:
        """Get comments by user."""
        result = await db.execute(
            select(DiscussionComment)
            .where(DiscussionComment.user_id == user_id)
            .options(selectinload(DiscussionComment.discussion))
            .order_by(desc(DiscussionComment.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


# Global instances
discussion_crud = CRUDDiscussion(Discussion)
comment_crud = CRUDComment(DiscussionComment)
