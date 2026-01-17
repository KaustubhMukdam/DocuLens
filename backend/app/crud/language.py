# ============================================================================
# app/crud/language.py
# ============================================================================
"""Language CRUD operations."""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language import Language
from app.schemas.language import LanguageCreate, LanguageUpdate
from app.crud.base import CRUDBase


class CRUDLanguage(CRUDBase[Language, LanguageCreate, LanguageUpdate]):
    """CRUD operations for Language model."""
    
    async def get_by_slug(
        self,
        db: AsyncSession,
        *,
        slug: str
    ) -> Optional[Language]:
        """Get language by slug."""
        result = await db.execute(
            select(Language).where(Language.slug == slug)
        )
        return result.scalar_one_or_none()
    
    async def get_active(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[Language]:
        """Get active languages."""
        result = await db.execute(
            select(Language)
            .where(Language.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

