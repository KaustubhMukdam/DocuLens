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

from loguru import logger
from app.core.exceptions import NotFoundException

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
async def get_language_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a programming language by slug.
    
    Returns:
    - Language metadata
    - Section statistics (total, quick path, deep path)
    - Estimated learning time
    """
    from sqlalchemy import select, func
    from app.models.doc_section import DocSection
    
    # Get language
    language = await language_crud.get_by_slug(db, slug=slug)
    if not language:
        raise NotFoundException(message=f"Language '{slug}' not found")
    
    # Count sections - FIX: Use proper async query
    total_sections_result = await db.execute(
        select(func.count(DocSection.id)).where(DocSection.language_id == language.id)
    )
    total_sections = total_sections_result.scalar_one()
    
    # Count quick path sections
    quick_path_result = await db.execute(
        select(func.count(DocSection.id)).where(
            DocSection.language_id == language.id,
            DocSection.is_quick_path == True
        )
    )
    quick_path_sections = quick_path_result.scalar_one()
    
    # Count deep path sections
    deep_path_result = await db.execute(
        select(func.count(DocSection.id)).where(
            DocSection.language_id == language.id,
            DocSection.is_deep_path == True
        )
    )
    deep_path_sections = deep_path_result.scalar_one()
    
    # Calculate estimated time (quick path)
    quick_time_result = await db.execute(
        select(func.sum(DocSection.estimated_time_minutes)).where(
            DocSection.language_id == language.id,
            DocSection.is_quick_path == True
        )
    )
    quick_time_minutes = quick_time_result.scalar_one() or 0
    
    # Calculate estimated time (deep path)
    deep_time_result = await db.execute(
        select(func.sum(DocSection.estimated_time_minutes)).where(
            DocSection.language_id == language.id,
            DocSection.is_deep_path == True
        )
    )
    deep_time_minutes = deep_time_result.scalar_one() or 0
    
    logger.info(f"Retrieved language '{slug}': {total_sections} sections")
    
    return LanguageDetailResponse(
        id=language.id,
        name=language.name,
        slug=language.slug,
        official_doc_url=language.official_doc_url,
        logo_url=language.logo_url,
        description=language.description,
        version=language.version,
        is_active=language.is_active,
        last_updated=language.last_updated,
        created_at=language.created_at,
        total_sections=total_sections,
        quick_path_sections=quick_path_sections,
        deep_path_sections=deep_path_sections,
        estimated_quick_time_hours=round(quick_time_minutes / 60, 1),
        estimated_deep_time_hours=round(deep_time_minutes / 60, 1)
    )