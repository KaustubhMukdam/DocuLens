# ============================================================================
# app/api/v1/languages.py
# ============================================================================
"""Language endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.language import LanguageResponse, LanguageDetailResponse
from app.schemas.response import PaginatedResponse, PaginationMeta
from app.crud import language as language_crud
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=PaginatedResponse[LanguageResponse])
async def get_languages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: AsyncSession = Depends(get_db)
):
    """Get all programming languages."""
    skip = (page - 1) * page_size
    
    languages = await language_crud.get_active(db=db, skip=skip, limit=page_size)
    total = await language_crud.count(db=db)
    
    total_pages = (total + page_size - 1) // page_size
    
    return PaginatedResponse(
        data=[LanguageResponse.model_validate(lang) for lang in languages],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    )


@router.get("/{slug}", response_model=LanguageDetailResponse)
async def get_language(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get language details by slug."""
    language = await language_crud.get_by_slug(db=db, slug=slug)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{slug}' not found"
        )
    
    # TODO: Calculate statistics
    response = LanguageDetailResponse.model_validate(language)
    response.total_sections = 0
    response.quick_path_sections = 0
    response.deep_path_sections = 0
    response.estimated_quick_time_hours = 0.0
    response.estimated_deep_time_hours = 0.0
    
    return response
