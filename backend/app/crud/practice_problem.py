# ============================================================================
# app/crud/practice_problem.py
# ============================================================================
"""Practice problem CRUD operations."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.practice_problem import PracticeProblem
from app.crud.base import CRUDBase
from pydantic import BaseModel


class PracticeProblemCreate(BaseModel):
    """Schema for creating practice problem."""
    doc_section_id: UUID
    title: str
    platform: str = "leetcode"
    difficulty: str = "medium"
    problem_url: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    order_index: int = 0


class PracticeProblemUpdate(BaseModel):
    """Schema for updating practice problem."""
    title: Optional[str] = None
    difficulty: Optional[str] = None
    problem_url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    order_index: Optional[int] = None


class CRUDPracticeProblem(CRUDBase[PracticeProblem, PracticeProblemCreate, PracticeProblemUpdate]):
    """CRUD operations for PracticeProblem model."""
    
    async def get_by_section(
        self,
        db: AsyncSession,
        *,
        section_id: UUID,
        difficulty: Optional[str] = None
    ) -> List[PracticeProblem]:
        """Get all practice problems for a section."""
        query = select(PracticeProblem).where(
            PracticeProblem.doc_section_id == section_id
        )
        
        if difficulty:
            query = query.where(PracticeProblem.difficulty == difficulty)
        
        query = query.order_by(PracticeProblem.order_index)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_language(
        self,
        db: AsyncSession,
        *,
        language_id: UUID,
        difficulty: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[PracticeProblem]:
        """Get all practice problems for a language."""
        from app.models.doc_section import DocSection
        
        query = (
            select(PracticeProblem)
            .join(DocSection)
            .where(DocSection.language_id == language_id)
        )
        
        if difficulty:
            query = query.where(PracticeProblem.difficulty == difficulty)
        
        query = query.order_by(desc(PracticeProblem.created_at)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())


# Global instance
practice_problem_crud = CRUDPracticeProblem(PracticeProblem)
