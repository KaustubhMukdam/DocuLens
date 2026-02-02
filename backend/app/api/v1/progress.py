# ============================================================================
# app/api/v1/progress.py
# ============================================================================
"""User progress tracking endpoints."""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, Field

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.language import (
    MarkCompleteRequest,
    UserProgressResponse,
    ProgressStatsResponse
)
from app.schemas.response import SuccessResponse
from app.crud.progress import progress_crud
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.core.logging import logger
from app.models.user_progress import UserProgress

router = APIRouter()
doc_section_crud = CRUDDocSection(DocSection)


# ============================================================================
# Request/Response Schemas
# ============================================================================

class MarkSectionCompleteRequest(BaseModel):
    """Request body for marking a section complete."""
    time_spent_seconds: int = Field(default=0, ge=0)
    notes: Optional[str] = Field(default=None, max_length=1000)


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/sections/{section_id}/complete", response_model=UserProgressResponse, status_code=status.HTTP_201_CREATED)
async def mark_section_complete_by_id(
    section_id: UUID,
    request: MarkSectionCompleteRequest = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a documentation section as completed (route-based).
    This endpoint accepts the section ID in the URL path.
    
    Records:
    - Section completion
    - Time spent on the section
    - Optional notes
    
    Updates learning path progress automatically.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )

    # Mark completed
    progress = await progress_crud.mark_completed(
        db,
        user_id=current_user.id,
        section_id=section_id,
        time_spent_seconds=request.time_spent_seconds,
        notes=request.notes
    )

    await db.commit()
    await db.refresh(progress)

    logger.info(
        f"User {current_user.id} completed section {section_id} "
        f"in {request.time_spent_seconds}s"
    )

    return UserProgressResponse.model_validate(progress)


@router.post("/mark-complete", response_model=UserProgressResponse, status_code=status.HTTP_201_CREATED)
async def mark_section_complete(
    request: MarkCompleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a documentation section as completed (body-based).
    This is the legacy endpoint that accepts section ID in request body.
    
    Records:
    - Section completion
    - Time spent on the section
    - Optional notes
    
    Updates learning path progress automatically.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=request.doc_section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )

    # Mark completed
    progress = await progress_crud.mark_completed(
        db,
        user_id=current_user.id,
        section_id=request.doc_section_id,
        time_spent_seconds=request.time_spent_seconds,
        notes=request.notes
    )

    await db.commit()
    await db.refresh(progress)

    logger.info(
        f"User {current_user.id} completed section {request.doc_section_id} "
        f"in {request.time_spent_seconds}s"
    )

    return UserProgressResponse.model_validate(progress)


@router.get("/me", response_model=List[UserProgressResponse])
async def get_my_progress(
    language_id: Optional[UUID] = Query(None, description="Filter by language"),
    completed_only: bool = Query(False, description="Show only completed sections"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get progress records for the current user.
    
    Optional filters:
    - language_id: Show progress for specific language only
    - completed_only: Show only completed sections
    """
    progress_records = await progress_crud.get_user_progress(
        db,
        user_id=current_user.id,
        language_id=language_id,
        completed_only=completed_only,
        skip=skip,
        limit=limit
    )

    return [UserProgressResponse.model_validate(p) for p in progress_records]


@router.get("/stats", response_model=ProgressStatsResponse)
async def get_progress_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive progress statistics for the current user.
    
    Includes:
    - Total time spent learning
    - Sections completed
    - Current and longest learning streaks
    - Number of languages being learned
    - Active and completed learning paths
    - Achievements unlocked
    """
    stats = await progress_crud.get_stats(db, user_id=current_user.id)
    return ProgressStatsResponse(**stats)


@router.get("/section/{section_id}", response_model=UserProgressResponse)
async def get_section_progress(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get progress for a specific section.
    Returns 404 if no progress recorded yet.
    """
    progress = await progress_crud.get_by_user_and_section(
        db,
        user_id=current_user.id,
        section_id=section_id
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress recorded for this section"
        )

    return UserProgressResponse.model_validate(progress)


@router.delete("/section/{section_id}", response_model=SuccessResponse)
async def reset_section_progress(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reset progress for a specific section.
    Useful if user wants to re-learn a section.
    """
    progress = await progress_crud.get_by_user_and_section(
        db,
        user_id=current_user.id,
        section_id=section_id
    )

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress to reset"
        )

    await db.delete(progress)
    await db.commit()

    logger.info(f"User {current_user.id} reset progress for section {section_id}")

    return SuccessResponse(
        message="Section progress reset successfully",
        data={"section_id": str(section_id)}
    )

@router.get("/recent-sections")
async def get_recent_sections(
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get recently viewed/completed sections by user.
    Returns the last N sections the user interacted with.
    """
    from app.models.doc_section import DocSection
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(UserProgress)
        .where(UserProgress.user_id == current_user.id)
        .options(
            selectinload(UserProgress.doc_section).selectinload(DocSection.language)
        )
        .order_by(desc(UserProgress.updated_at))
        .limit(limit)
    )
    
    recent_progress = result.scalars().all()
    
    return [
        {
            "section_id": str(p.doc_section_id),
            "section_title": p.doc_section.title,
            "section_slug": p.doc_section.slug,
            "language_name": p.doc_section.language.name if p.doc_section.language else "Unknown",
            "language_slug": p.doc_section.language.slug if p.doc_section.language else "unknown",
            "is_completed": p.is_completed,
            "time_spent_seconds": p.time_spent_seconds,
            "last_accessed": p.updated_at,
        }
        for p in recent_progress
    ]