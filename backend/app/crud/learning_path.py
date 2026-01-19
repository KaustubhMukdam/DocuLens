# ============================================================================
# app/crud/learning_path.py
# ============================================================================
"""Learning path CRUD operations."""

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.learning_path import LearningPath, PathType, PathStatus
from app.schemas.language import LearningPathCreate, LearningPathUpdate
from app.crud.base import CRUDBase


class CRUDLearningPath(CRUDBase[LearningPath, LearningPathCreate, LearningPathUpdate]):
    """CRUD operations for LearningPath model."""
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[LearningPath]:
        """Get all learning paths for a user."""
        result = await db.execute(
            select(LearningPath)
            .where(LearningPath.user_id == user_id)
            .options(selectinload(LearningPath.language))
            .order_by(LearningPath.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_user_and_language(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        language_id: UUID,
        path_type: Optional[str] = None
    ) -> Optional[LearningPath]:
        """Get learning path for user and language."""
        query = select(LearningPath).where(
            and_(
                LearningPath.user_id == user_id,
                LearningPath.language_id == language_id
            )
        ).options(selectinload(LearningPath.language))
        
        if path_type:
            query = query.where(LearningPath.path_type == PathType(path_type))
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_active_paths(
        self,
        db: AsyncSession,
        *,
        user_id: UUID
    ) -> List[LearningPath]:
        """Get all active (in progress) learning paths for user."""
        result = await db.execute(
            select(LearningPath)
            .where(
                and_(
                    LearningPath.user_id == user_id,
                    LearningPath.status == PathStatus.IN_PROGRESS
                )
            )
            .options(selectinload(LearningPath.language))
            .order_by(LearningPath.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_completed_paths(
        self,
        db: AsyncSession,
        *,
        user_id: UUID
    ) -> List[LearningPath]:
        """Get all completed learning paths for user."""
        result = await db.execute(
            select(LearningPath)
            .where(
                and_(
                    LearningPath.user_id == user_id,
                    LearningPath.status == PathStatus.COMPLETED
                )
            )
            .options(selectinload(LearningPath.language))
            .order_by(LearningPath.completed_at.desc())
        )
        return list(result.scalars().all())
    
    async def count_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        status: Optional[PathStatus] = None
    ) -> int:
        """Count learning paths for user."""
        query = select(func.count()).select_from(LearningPath).where(
            LearningPath.user_id == user_id
        )
        
        if status:
            query = query.where(LearningPath.status == status)
        
        result = await db.execute(query)
        return result.scalar_one()
    
    async def update_progress(
        self,
        db: AsyncSession,
        *,
        path_id: UUID,
        progress_percentage: float,
        status: Optional[PathStatus] = None
    ) -> Optional[LearningPath]:
        """Update learning path progress."""
        path = await self.get(db, id=path_id)
        if not path:
            return None
        
        path.progress_percentage = progress_percentage
        
        # Update status based on progress
        if progress_percentage == 0:
            path.status = PathStatus.NOT_STARTED
            path.started_at = None
        elif progress_percentage >= 100:
            path.status = PathStatus.COMPLETED
            from datetime import datetime
            path.completed_at = datetime.utcnow()
        else:
            if path.status == PathStatus.NOT_STARTED:
                from datetime import datetime
                path.started_at = datetime.utcnow()
            path.status = PathStatus.IN_PROGRESS
        
        # Override status if explicitly provided
        if status:
            path.status = status
        
        await db.flush()
        await db.refresh(path)
        return path


# Global instance
learning_path_crud = CRUDLearningPath(LearningPath)
