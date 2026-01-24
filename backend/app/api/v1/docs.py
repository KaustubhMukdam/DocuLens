# ============================================================================
# app/api/v1/docs.py
# ============================================================================
"""Documentation endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.api.deps import get_db, get_optional_current_user
from app.schemas.doc_section import (
    DocSectionResponse,
    DocSectionDetailResponse,
    DocSectionSummary
)
from app.schemas.response import PaginatedResponse, PaginationMeta
from app.crud import doc_section as doc_crud, language as lang_crud
from app.models.user import User
from app.models.doc_section import DocSection
from app.models.user_progress import UserProgress
from app.core.config import settings

router = APIRouter()

@router.get("/{language_slug}/sections", response_model=List[DocSectionSummary])
async def get_language_sections(
    language_slug: str,
    path_type: Optional[str] = Query(None, pattern="^(quick|deep)$"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get all sections for a language, optionally filtered by path type."""
    # Get language
    language = await lang_crud.get_by_slug(db=db, slug=language_slug)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{language_slug}' not found"
        )
    
    # Get sections based on path type
    if path_type == "quick":
        sections = await doc_crud.get_quick_path(db=db, language_id=language.id)
    elif path_type == "deep":
        sections = await doc_crud.get_deep_path(db=db, language_id=language.id)
    else:
        sections = await doc_crud.get_by_language(db=db, language_id=language.id)
    
    # TODO: Check user progress for is_completed flag
    return [DocSectionSummary.model_validate(section) for section in sections]


@router.get("/sections/{section_id}", response_model=DocSectionDetailResponse)
async def get_section_detail(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Get detailed section content."""
    # Build query with eager loading to prevent MissingGreenlet error
    query = (
        select(DocSection)
        .options(
            selectinload(DocSection.code_examples),
            selectinload(DocSection.video_resources),
            selectinload(DocSection.language)
        )
        .where(DocSection.id == section_id)
    )
    
    result = await db.execute(query)
    section = result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Check if completed by current user
    is_completed = False
    if current_user:
        progress_query = select(UserProgress).where(
            UserProgress.user_id == current_user.id,
            UserProgress.doc_section_id == section_id,
            UserProgress.is_completed == True
        )
        progress_result = await db.execute(progress_query)
        is_completed = progress_result.scalar_one_or_none() is not None
    
    # Convert to dict and add is_completed
    # In your docs.py file, update the section_dict to include parent_id:
    section_dict = {
        "id": section.id,
        "language_id": section.language_id,
        "parent_id": section.parent_id,
        "title": section.title,
        "slug": section.slug,
        "content_raw": section.content_raw,
        "content_summary": section.content_summary,
        "source_url": section.source_url,
        "order_index": section.order_index,
        "estimated_time_minutes": section.estimated_time_minutes,
        "difficulty": section.difficulty,
        "is_quick_path": section.is_quick_path,
        "is_deep_path": section.is_deep_path,
        "created_at": section.created_at,
        "updated_at": section.updated_at,
        "is_completed": is_completed,
        "code_examples": section.code_examples,
        "video_resources": section.video_resources,
        "children": []
    }

    
    return DocSectionDetailResponse(**section_dict)
