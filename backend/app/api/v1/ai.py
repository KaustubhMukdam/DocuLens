# ============================================================================
# app/api/v1/ai.py
# ============================================================================
"""AI endpoints for summarization and roadmap generation."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.doc_section import DocSection
from app.services.ai_services import ai_service
from app.crud.doc_section import CRUDDocSection
from app.schemas.response import SuccessResponse
from app.core.exceptions import ServiceUnavailableException, BadRequestException
from app.core.logging import logger
from pydantic import BaseModel, Field

router = APIRouter()

# Initialize CRUD
doc_section_crud = CRUDDocSection(DocSection)


# ============================================================================
# Schemas
# ============================================================================

class SummarizeRequest(BaseModel):
    """Request to summarize content."""
    content: str = Field(..., min_length=50, max_length=50000, description="Content to summarize")
    max_length: int = Field(500, ge=100, le=2000, description="Maximum summary length in words")
    style: str = Field("concise", pattern="^(concise|detailed|bullet_points)$", description="Summary style")
    language_context: Optional[str] = Field(None, max_length=50, description="Programming language context")


class SummarizeResponse(BaseModel):
    """Response with summarized content."""
    summary: str = Field(..., description="Summarized content")
    original_length: int = Field(..., description="Original content length in characters")
    summary_length: int = Field(..., description="Summary length in characters")
    compression_ratio: float = Field(..., description="Compression ratio (0-1)")


class RoadmapRequest(BaseModel):
    """Request to generate learning roadmap."""
    language_slug: str = Field(..., max_length=100, description="Programming language slug")
    skill_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$", description="User skill level")
    available_hours_per_week: int = Field(..., ge=1, le=40, description="Available hours per week")
    learning_goal: Optional[str] = Field(None, max_length=200, description="Specific learning goal")
    path_type: str = Field("balanced", pattern="^(quick|balanced|deep)$", description="Learning path type")


class RoadmapResponse(BaseModel):
    """Response with generated roadmap."""
    language_name: str
    language_slug: str
    total_weeks: int
    weekly_schedule: list
    milestones: list[str]
    estimated_completion_date: str
    note: Optional[str] = None


class AutoSummarizeResponse(BaseModel):
    """Response after auto-summarizing a section."""
    section_id: UUID
    title: str
    summary: str
    compression_ratio: float
    updated: bool


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_content(
    request: SummarizeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Summarize documentation content using AI.
    
    - **content**: Raw documentation content (50-50,000 chars)
    - **max_length**: Maximum summary length in words (100-2000)
    - **style**: Summary style (concise, detailed, bullet_points)
    - **language_context**: Programming language context for better results
    
    Returns summarized content with statistics.
    """
    try:
        logger.info(f"User {current_user.id} requested content summarization")
        
        # Generate summary
        summary = await ai_service.summarize_documentation(
            content=request.content,
            max_length=request.max_length,
            style=request.style,
            language_context=request.language_context
        )
        
        # Calculate statistics
        original_length = len(request.content)
        summary_length = len(summary)
        compression_ratio = round(summary_length / original_length, 3)
        
        logger.info(f"Summary generated: {original_length} -> {summary_length} chars")
        
        return SummarizeResponse(
            summary=summary,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio
        )
    
    except BadRequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except ServiceUnavailableException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=e.message
        )
    except Exception as e:
        logger.exception(f"Summarization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Summarization failed"
        )


@router.post("/sections/{section_id}/auto-summarize", response_model=AutoSummarizeResponse)
async def auto_summarize_section(
    section_id: UUID,
    max_length: int = Body(500, ge=100, le=2000),
    style: str = Body("concise", pattern="^(concise|detailed|bullet_points)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Automatically summarize a documentation section and update it.
    
    This endpoint:
    1. Fetches the section by ID
    2. Generates AI summary from content_raw
    3. Updates content_summary field
    4. Returns the updated section
    
    Requires authentication. Only works on existing sections.
    """
    # Get section
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section {section_id} not found"
        )
    
    try:
        logger.info(f"Auto-summarizing section {section_id} for user {current_user.id}")
        
        # Get language context
        language_context = None
        if section.language:
            language_context = section.language.name
        
        # Generate summary
        summary = await ai_service.summarize_documentation(
            content=section.content_raw,
            max_length=max_length,
            style=style,
            language_context=language_context
        )
        
        # Update section
        section.content_summary = summary
        await db.commit()
        await db.refresh(section)
        
        # Calculate compression
        compression_ratio = round(len(summary) / len(section.content_raw), 3)
        
        logger.info(f"Section {section_id} summarized and updated")
        
        return AutoSummarizeResponse(
            section_id=section.id,
            title=section.title,
            summary=summary,
            compression_ratio=compression_ratio,
            updated=True
        )
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Auto-summarization failed for section {section_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auto-summarization failed"
        )


@router.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(
    request: RoadmapRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a personalized learning roadmap using AI.
    
    Creates a custom learning plan based on:
    - Programming language
    - User's skill level
    - Available study time
    - Learning goals
    - Preferred path type (quick/balanced/deep)
    
    Returns a structured roadmap with weekly schedule and milestones.
    """
    from app.crud.language import CRUDLanguage
    from app.models.language import Language
    
    language_crud = CRUDLanguage(Language)
    
    # Verify language exists
    language = await language_crud.get_by_slug(db, slug=request.language_slug)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{request.language_slug}' not found"
        )
    
    try:
        logger.info(
            f"Generating roadmap for {current_user.id}: "
            f"{language.name}, {request.skill_level}, {request.path_type}"
        )
        
        # Generate roadmap
        roadmap = await ai_service.generate_learning_roadmap(
            language_name=language.name,
            skill_level=request.skill_level,
            available_hours_per_week=request.available_hours_per_week,
            learning_goal=request.learning_goal,
            path_type=request.path_type
        )
        
        logger.info(f"Roadmap generated: {roadmap.get('total_weeks')} weeks")
        
        return RoadmapResponse(
            language_name=language.name,
            language_slug=language.slug,
            **roadmap
        )
    
    except Exception as e:
        logger.exception(f"Roadmap generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate roadmap"
        )


@router.post("/batch-summarize")
async def batch_summarize_sections(
    language_slug: str = Body(...),
    max_sections: int = Body(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Batch summarize all sections for a language that don't have summaries.
    
    This is useful for bulk processing when adding a new language.
    Limited to prevent abuse.
    
    **Admin/Premium feature** - Add authorization check as needed.
    """
    from app.crud.language import CRUDLanguage
    from app.models.language import Language
    from sqlalchemy import select, and_
    
    language_crud = CRUDLanguage(Language)
    
    # Get language
    language = await language_crud.get_by_slug(db, slug=language_slug)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{language_slug}' not found"
        )
    
    # TODO: Add premium/admin check here
    # if not current_user.is_premium and not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Premium feature")
    
    try:
        # Get sections without summaries
        result = await db.execute(
            select(DocSection)
            .where(
                and_(
                    DocSection.language_id == language.id,
                    DocSection.content_summary.is_(None)
                )
            )
            .limit(max_sections)
        )
        sections = list(result.scalars().all())
        
        if not sections:
            return SuccessResponse(
                message="No sections need summarization",
                data={"language": language_slug, "processed": 0}
            )
        
        logger.info(f"Batch summarizing {len(sections)} sections for {language_slug}")
        
        # Summarize each section
        summarized_count = 0
        failed_count = 0
        
        for section in sections:
            try:
                summary = await ai_service.summarize_documentation(
                    content=section.content_raw,
                    max_length=500,
                    style="concise",
                    language_context=language.name
                )
                section.content_summary = summary
                summarized_count += 1
            except Exception as e:
                logger.error(f"Failed to summarize section {section.id}: {e}")
                failed_count += 1
        
        # Commit all changes
        await db.commit()
        
        logger.info(
            f"Batch summarization complete: {summarized_count} success, {failed_count} failed"
        )
        
        return SuccessResponse(
            message="Batch summarization complete",
            data={
                "language": language_slug,
                "total_sections": len(sections),
                "summarized": summarized_count,
                "failed": failed_count
            }
        )
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Batch summarization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch summarization failed"
        )
