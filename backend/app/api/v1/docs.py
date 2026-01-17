# ============================================================================
# app/api/v1/docs.py
# ============================================================================
"""Documentation endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
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
from app.core.config import settings

router = APIRouter()


@router.get("/{language_slug}/sections", response_model=List[DocSectionSummary])
async def get_language_sections(
    language_slug: str,
    path_type: Optional[str] = Query(None, regex="^(quick|deep)$"),
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
    section = await doc_crud.get(db=db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # TODO: Add code examples, next/prev sections
    response = DocSectionDetailResponse.model_validate(section)
    return response