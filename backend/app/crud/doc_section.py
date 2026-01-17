# ============================================================================
# app/crud/doc_section.py
# ============================================================================
"""Documentation section CRUD operations."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.doc_section import DocSection
from app.schemas.doc_section import DocSectionCreate, DocSectionUpdate
from app.crud.base import CRUDBase


class CRUDDocSection(CRUDBase[DocSection, DocSectionCreate, DocSectionUpdate]):
    """CRUD operations for DocSection model."""
    
    async def get_by_language(
        self,
        db: AsyncSession,
        *,
        language_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[DocSection]:
        """Get sections by language."""
        result = await db.execute(
            select(DocSection)
            .where(DocSection.language_id == language_id)
            .order_by(DocSection.order_index)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_slug(
        self,
        db: AsyncSession,
        *,
        language_id: UUID,
        slug: str
    ) -> Optional[DocSection]:
        """Get section by language and slug."""
        result = await db.execute(
            select(DocSection).where(
                and_(
                    DocSection.language_id == language_id,
                    DocSection.slug == slug
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_quick_path(
        self,
        db: AsyncSession,
        *,
        language_id: UUID
    ) -> List[DocSection]:
        """Get quick path sections."""
        result = await db.execute(
            select(DocSection)
            .where(
                and_(
                    DocSection.language_id == language_id,
                    DocSection.is_quick_path == True
                )
            )
            .order_by(DocSection.order_index)
        )
        return list(result.scalars().all())
    
    async def get_deep_path(
        self,
        db: AsyncSession,
        *,
        language_id: UUID
    ) -> List[DocSection]:
        """Get deep path sections."""
        result = await db.execute(
            select(DocSection)
            .where(
                and_(
                    DocSection.language_id == language_id,
                    DocSection.is_deep_path == True
                )
            )
            .order_by(DocSection.order_index)
        )
        return list(result.scalars().all())