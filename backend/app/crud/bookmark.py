# ============================================================================
# app/crud/bookmark.py
# ============================================================================
"""Bookmark CRUD operations."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.bookmark import Bookmark
from app.crud.base import CRUDBase
from pydantic import BaseModel


class BookmarkCreate(BaseModel):
    """Schema for creating bookmark."""
    doc_section_id: UUID
    notes: Optional[str] = None


class BookmarkUpdate(BaseModel):
    """Schema for updating bookmark."""
    notes: Optional[str] = None


class CRUDBookmark(CRUDBase[Bookmark, BookmarkCreate, BookmarkUpdate]):
    """CRUD operations for Bookmark model."""
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        language_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Bookmark]:
        """Get all bookmarks for a user."""
        from app.models.doc_section import DocSection
        
        query = (
            select(Bookmark)
            .where(Bookmark.user_id == user_id)
            .options(selectinload(Bookmark.doc_section))
            .order_by(desc(Bookmark.created_at))
        )
        
        if language_id:
            query = query.join(DocSection).where(DocSection.language_id == language_id)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_user_and_section(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        section_id: UUID
    ) -> Optional[Bookmark]:
        """Check if user has bookmarked a section."""
        result = await db.execute(
            select(Bookmark).where(
                and_(
                    Bookmark.user_id == user_id,
                    Bookmark.doc_section_id == section_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def create_bookmark(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        section_id: UUID,
        notes: Optional[str] = None
    ) -> Bookmark:
        """Create a bookmark."""
        # Check if already bookmarked
        existing = await self.get_by_user_and_section(
            db, user_id=user_id, section_id=section_id
        )
        if existing:
            return existing
        
        bookmark = Bookmark(
            user_id=user_id,
            doc_section_id=section_id,
            notes=notes
        )
        db.add(bookmark)
        await db.flush()
        await db.refresh(bookmark)
        return bookmark
    
    async def delete_bookmark(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        section_id: UUID
    ) -> bool:
        """Delete a bookmark."""
        bookmark = await self.get_by_user_and_section(
            db, user_id=user_id, section_id=section_id
        )
        if not bookmark:
            return False
        
        await db.delete(bookmark)
        await db.flush()
        return True
    
    async def count_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID
    ) -> int:
        """Count bookmarks for a user."""
        from sqlalchemy import func
        result = await db.execute(
            select(func.count())
            .select_from(Bookmark)
            .where(Bookmark.user_id == user_id)
        )
        return result.scalar_one()


# Global instance
bookmark_crud = CRUDBookmark(Bookmark)
