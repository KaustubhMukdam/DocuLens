# ============================================================================
# app/crud/progress.py
# ============================================================================
"""User progress CRUD operations."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_progress import UserProgress
from app.crud.base import CRUDBase
from pydantic import BaseModel


class ProgressCreate(BaseModel):
    """Schema for creating progress record."""
    doc_section_id: UUID
    time_spent_seconds: int = 0
    is_completed: bool = False
    notes: Optional[str] = None


class ProgressUpdate(BaseModel):
    """Schema for updating progress record."""
    time_spent_seconds: Optional[int] = None
    is_completed: Optional[bool] = None
    notes: Optional[str] = None


class CRUDProgress(CRUDBase[UserProgress, ProgressCreate, ProgressUpdate]):
    """CRUD operations for UserProgress model."""
    
    async def get_by_user_and_section(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        section_id: UUID
    ) -> Optional[UserProgress]:
        """Get progress record for user and section."""
        result = await db.execute(
            select(UserProgress).where(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.doc_section_id == section_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_progress(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        language_id: Optional[UUID] = None,
        completed_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserProgress]:
        """Get all progress records for a user."""
        from app.models.doc_section import DocSection
        
        query = select(UserProgress).where(UserProgress.user_id == user_id)
        
        if language_id:
            query = query.join(DocSection).where(DocSection.language_id == language_id)
        
        if completed_only:
            query = query.where(UserProgress.is_completed == True)
        
        query = query.order_by(desc(UserProgress.updated_at)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def mark_completed(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        section_id: UUID,
        time_spent_seconds: int,
        notes: Optional[str] = None
    ) -> UserProgress:
        """Mark a section as completed."""
        # Get or create progress record
        progress = await self.get_by_user_and_section(
            db, user_id=user_id, section_id=section_id
        )
        
        if progress:
            # Update existing
            progress.is_completed = True
            progress.time_spent_seconds += time_spent_seconds
            progress.completed_at = datetime.utcnow()
            if notes:
                progress.notes = notes
        else:
            # Create new
            progress = UserProgress(
                user_id=user_id,
                doc_section_id=section_id,
                is_completed=True,
                time_spent_seconds=time_spent_seconds,
                completed_at=datetime.utcnow(),
                notes=notes
            )
            db.add(progress)
        
        await db.flush()
        await db.refresh(progress)
        return progress
    
    async def get_stats(
        self,
        db: AsyncSession,
        *,
        user_id: UUID
    ) -> dict:
        """Get progress statistics for a user."""
        # Total time spent
        total_time_result = await db.execute(
            select(func.sum(UserProgress.time_spent_seconds))
            .where(UserProgress.user_id == user_id)
        )
        total_seconds = total_time_result.scalar_one() or 0
        
        # Sections completed
        completed_result = await db.execute(
            select(func.count())
            .select_from(UserProgress)
            .where(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.is_completed == True
                )
            )
        )
        sections_completed = completed_result.scalar_one()
        
        # Calculate streaks
        current_streak = await self._calculate_current_streak(db, user_id)
        longest_streak = await self._calculate_longest_streak(db, user_id)
        
        # Languages being learned (with progress)
        from app.models.doc_section import DocSection
        from app.models.language import Language
        
        languages_result = await db.execute(
            select(func.count(func.distinct(Language.id)))
            .select_from(UserProgress)
            .join(DocSection)
            .join(Language)
            .where(UserProgress.user_id == user_id)
        )
        languages_learning = languages_result.scalar_one()
        
        # Active and completed paths
        from app.models.learning_path import LearningPath, PathStatus
        
        active_paths_result = await db.execute(
            select(func.count())
            .select_from(LearningPath)
            .where(
                and_(
                    LearningPath.user_id == user_id,
                    LearningPath.status == PathStatus.IN_PROGRESS
                )
            )
        )
        active_paths = active_paths_result.scalar_one()
        
        completed_paths_result = await db.execute(
            select(func.count())
            .select_from(LearningPath)
            .where(
                and_(
                    LearningPath.user_id == user_id,
                    LearningPath.status == PathStatus.COMPLETED
                )
            )
        )
        completed_paths = completed_paths_result.scalar_one()
        
        return {
            "total_time_seconds": total_seconds,
            "total_time_hours": round(total_seconds / 3600, 1),
            "sections_completed": sections_completed,
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
            "languages_learning": languages_learning,
            "active_paths": active_paths,
            "completed_paths": completed_paths,
            "achievements": self._calculate_achievements(
                sections_completed, total_seconds, longest_streak
            )
        }
    
    async def _calculate_current_streak(self, db: AsyncSession, user_id: UUID) -> int:
        """Calculate current learning streak in days."""
        # Get recent completions
        result = await db.execute(
            select(func.date(UserProgress.completed_at))
            .where(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.is_completed == True,
                    UserProgress.completed_at.isnot(None)
                )
            )
            .distinct()
            .order_by(desc(func.date(UserProgress.completed_at)))
            .limit(30)
        )
        
        completion_dates = [date for (date,) in result.all() if date]
        
        if not completion_dates:
            return 0
        
        # Check if today or yesterday has activity
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        if completion_dates[0] not in [today, yesterday]:
            return 0
        
        # Count consecutive days
        streak = 1
        current_date = completion_dates[0]
        
        for date in completion_dates[1:]:
            expected_date = current_date - timedelta(days=1)
            if date == expected_date:
                streak += 1
                current_date = date
            else:
                break
        
        return streak
    
    async def _calculate_longest_streak(self, db: AsyncSession, user_id: UUID) -> int:
        """Calculate longest learning streak in days."""
        result = await db.execute(
            select(func.date(UserProgress.completed_at))
            .where(
                and_(
                    UserProgress.user_id == user_id,
                    UserProgress.is_completed == True,
                    UserProgress.completed_at.isnot(None)
                )
            )
            .distinct()
            .order_by(func.date(UserProgress.completed_at))
        )
        
        completion_dates = [date for (date,) in result.all() if date]
        
        if not completion_dates:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(completion_dates)):
            expected_date = completion_dates[i-1] + timedelta(days=1)
            if completion_dates[i] == expected_date:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak
    
    def _calculate_achievements(
        self, sections_completed: int, total_seconds: int, longest_streak: int
    ) -> List[str]:
        """Calculate user achievements based on stats."""
        achievements = []
        
        # Section milestones
        if sections_completed >= 100:
            achievements.append("Century Scholar - 100+ sections completed")
        elif sections_completed >= 50:
            achievements.append("Dedicated Learner - 50+ sections completed")
        elif sections_completed >= 10:
            achievements.append("Getting Started - 10+ sections completed")
        
        # Time milestones
        hours = total_seconds / 3600
        if hours >= 100:
            achievements.append("Time Master - 100+ hours of learning")
        elif hours >= 50:
            achievements.append("Committed Student - 50+ hours of learning")
        elif hours >= 10:
            achievements.append("Learning Journey - 10+ hours invested")
        
        # Streak achievements
        if longest_streak >= 30:
            achievements.append("30-Day Warrior - 30-day learning streak")
        elif longest_streak >= 7:
            achievements.append("Week Champion - 7-day learning streak")
        elif longest_streak >= 3:
            achievements.append("Consistency Builder - 3-day streak")
        
        return achievements


# Global instance
progress_crud = CRUDProgress(UserProgress)
