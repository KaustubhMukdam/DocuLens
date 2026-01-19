# ============================================================================
# app/api/v1/learning_paths.py
# ============================================================================
"""Learning path endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.learning_path import LearningPath, PathType, PathStatus
from app.models.language import Language
from app.models.doc_section import DocSection
from app.models.user_progress import UserProgress
from app.schemas.language import (
    LearningPathCreate,
    LearningPathUpdate,
    LearningPathResponse,
    LearningPathDetailResponse,
    DocSectionSummary
)
from app.schemas.response import SuccessResponse
from app.crud.learning_path import learning_path_crud
from app.crud.language import CRUDLanguage
from app.core.logging import logger

router = APIRouter()

# Initialize CRUD
language_crud = CRUDLanguage(Language)


@router.post("", response_model=LearningPathResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_path(
    path_data: LearningPathCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new learning path for the current user.
    
    - **language_id**: UUID of the programming language
    - **path_type**: Either "quick" or "deep"
    
    Creates a learning path that tracks user's progress through a language's documentation.
    Quick path includes only essential sections, Deep path includes comprehensive coverage.
    """
    # Check if language exists
    language = await language_crud.get(db, id=path_data.language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language {path_data.language_id} not found"
        )
    
    # Check if path already exists
    existing_path = await learning_path_crud.get_by_user_and_language(
        db,
        user_id=current_user.id,
        language_id=path_data.language_id,
        path_type=path_data.path_type
    )
    
    if existing_path:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Learning path already exists for {language.name} ({path_data.path_type})"
        )
    
    # Create learning path
    from app.schemas.language import LearningPathCreate as LPCreate
    create_data = LPCreate(
        language_id=path_data.language_id,
        path_type=path_data.path_type
    )
    
    # Manually create the path with user_id
    from datetime import datetime
    path = LearningPath(
        user_id=current_user.id,
        language_id=path_data.language_id,
        path_type=PathType(path_data.path_type),
        status=PathStatus.NOT_STARTED,
        progress_percentage=0.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(path)
    await db.commit()
    await db.refresh(path)
    
    logger.info(
        f"User {current_user.id} created {path_data.path_type} path for {language.name}"
    )
    
    return LearningPathResponse.model_validate(path)


@router.get("/me", response_model=List[LearningPathResponse])
async def get_my_learning_paths(
    status_filter: Optional[str] = Query(None, pattern="^(not_started|in_progress|completed)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all learning paths for the current user.
    
    Optional filter by status:
    - not_started
    - in_progress
    - completed
    """
    if status_filter:
        if status_filter == "in_progress":
            paths = await learning_path_crud.get_active_paths(db, user_id=current_user.id)
        elif status_filter == "completed":
            paths = await learning_path_crud.get_completed_paths(db, user_id=current_user.id)
        else:
            # Get paths with specific status
            result = await db.execute(
                select(LearningPath)
                .where(
                    and_(
                        LearningPath.user_id == current_user.id,
                        LearningPath.status == PathStatus(status_filter)
                    )
                )
            )
            paths = list(result.scalars().all())
    else:
        paths = await learning_path_crud.get_by_user(db, user_id=current_user.id)
    
    return [LearningPathResponse.model_validate(path) for path in paths]


@router.get("/{path_id}", response_model=LearningPathDetailResponse)
async def get_learning_path_detail(
    path_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about a specific learning path.
    
    Includes:
    - Path metadata (progress, status, etc.)
    - List of sections in the path
    - Completion status for each section
    - Estimated time remaining
    """
    # Get path
    path = await learning_path_crud.get(db, id=path_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    # Verify ownership
    if path.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this learning path"
        )
    
    # Get language
    language = await language_crud.get(db, id=path.language_id)
    
    # Get sections based on path type
    is_quick_path = path.path_type == PathType.QUICK
    
    result = await db.execute(
        select(DocSection)
        .where(
            and_(
                DocSection.language_id == path.language_id,
                DocSection.is_quick_path == True if is_quick_path else DocSection.is_deep_path == True
            )
        )
        .order_by(DocSection.order_index)
    )
    sections = list(result.scalars().all())
    
    # Get user progress for these sections
    section_ids = [s.id for s in sections]
    progress_result = await db.execute(
        select(UserProgress)
        .where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.doc_section_id.in_(section_ids),
                UserProgress.is_completed == True
            )
        )
    )
    completed_section_ids = {p.doc_section_id for p in progress_result.scalars().all()}
    
    # Calculate statistics
    total_sections = len(sections)
    completed_sections = len(completed_section_ids)
    total_time_minutes = sum(s.estimated_time_minutes or 30 for s in sections)
    estimated_time_hours = round(total_time_minutes / 60, 1)
    
    # Build section summaries with completion status
    section_summaries = []
    for section in sections:
        summary = DocSectionSummary.model_validate(section)
        summary.is_completed = section.id in completed_section_ids
        section_summaries.append(summary)
    
    # Build detailed response
    response = LearningPathDetailResponse.model_validate(path)
    response.language_name = language.name
    response.language_slug = language.slug
    response.total_sections = total_sections
    response.completed_sections = completed_sections
    response.estimated_time_hours = estimated_time_hours
    response.sections = section_summaries
    
    return response


@router.put("/{path_id}/progress", response_model=LearningPathResponse)
async def update_path_progress(
    path_id: UUID,
    progress_percentage: float = Body(..., ge=0.0, le=100.0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually update progress percentage for a learning path.
    
    Progress is usually calculated automatically based on completed sections,
    but this endpoint allows manual adjustment if needed.
    """
    # Get path
    path = await learning_path_crud.get(db, id=path_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    # Verify ownership
    if path.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this learning path"
        )
    
    # Update progress
    updated_path = await learning_path_crud.update_progress(
        db,
        path_id=path_id,
        progress_percentage=progress_percentage
    )
    
    await db.commit()
    await db.refresh(updated_path)
    
    logger.info(f"Path {path_id} progress updated to {progress_percentage}%")
    
    return LearningPathResponse.model_validate(updated_path)


@router.delete("/{path_id}", response_model=SuccessResponse)
async def delete_learning_path(
    path_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a learning path.
    
    This does NOT delete the user's progress on individual sections,
    only the learning path tracker itself.
    """
    # Get path
    path = await learning_path_crud.get(db, id=path_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    # Verify ownership
    if path.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this learning path"
        )
    
    # Delete
    await learning_path_crud.delete(db, id=path_id)
    await db.commit()
    
    logger.info(f"Learning path {path_id} deleted by user {current_user.id}")
    
    return SuccessResponse(
        message="Learning path deleted successfully",
        data={"path_id": str(path_id)}
    )


@router.post("/{path_id}/start", response_model=LearningPathResponse)
async def start_learning_path(
    path_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a learning path as started.
    
    Sets status to IN_PROGRESS and records started_at timestamp.
    """
    path = await learning_path_crud.get(db, id=path_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )
    
    if path.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    if path.status != PathStatus.NOT_STARTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Path already {path.status.value}"
        )
    
    # Start the path
    from datetime import datetime
    path.status = PathStatus.IN_PROGRESS
    path.started_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(path)
    
    logger.info(f"User {current_user.id} started learning path {path_id}")
    
    return LearningPathResponse.model_validate(path)
