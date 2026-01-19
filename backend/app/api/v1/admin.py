# ============================================================================
# app/api/v1/admin.py
# ============================================================================
"""Admin endpoints for managing platform content."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from pydantic import BaseModel, HttpUrl

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.language import Language
from app.models.doc_section import DocSection, Difficulty
from app.models.video_resource import VideoResource
from app.models.practice_problem import PracticeProblem
from app.core.exceptions import ForbiddenException, NotFoundException, BadRequestException
from app.schemas.response import SuccessResponse
from app.core.logging import logger


from app.services.scraper_service import scraper_service

router = APIRouter()


# ============================================================================
# Dependency: Admin Only
# ============================================================================

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency to ensure user is admin."""
    if not current_user.is_admin:
        raise ForbiddenException(
            message="Admin access required",
            details={"required_role": "admin", "user_role": "user"}
        )
    return current_user


# ============================================================================
# Schemas
# ============================================================================

class LanguageCreateAdmin(BaseModel):
    """Schema for creating language (admin)."""
    name: str
    slug: str
    official_doc_url: HttpUrl
    description: Optional[str] = None
    version: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_active: bool = True


class LanguageUpdateAdmin(BaseModel):
    """Schema for updating language (admin)."""
    name: Optional[str] = None
    official_doc_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    version: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None


class DocSectionCreateAdmin(BaseModel):
    """Schema for creating doc section (admin)."""
    language_id: UUID
    title: str
    slug: str
    content_raw: str
    content_summary: Optional[str] = None
    source_url: HttpUrl
    parent_section_id: Optional[UUID] = None
    order_index: int = 0
    estimated_time_minutes: int = 30
    difficulty: Difficulty = Difficulty.MEDIUM
    is_quick_path: bool = False
    is_deep_path: bool = True


class DocSectionUpdateAdmin(BaseModel):
    """Schema for updating doc section (admin)."""
    title: Optional[str] = None
    content_raw: Optional[str] = None
    content_summary: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    order_index: Optional[int] = None
    estimated_time_minutes: Optional[int] = None
    difficulty: Optional[Difficulty] = None
    is_quick_path: Optional[bool] = None
    is_deep_path: Optional[bool] = None


class VideoResourceCreateAdmin(BaseModel):
    """Schema for adding video resource (admin)."""
    doc_section_id: UUID
    title: str
    url: HttpUrl
    platform: str = "youtube"
    duration_seconds: Optional[int] = None
    channel_name: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    order_index: int = 0


class PracticeProblemCreateAdmin(BaseModel):
    """Schema for adding practice problem (admin)."""
    doc_section_id: UUID
    title: str
    platform: str = "leetcode"
    difficulty: str = "medium"
    problem_url: HttpUrl
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    order_index: int = 0


class UserPromoteRequest(BaseModel):
    """Schema for promoting user to admin."""
    user_id: UUID


class AdminStatsResponse(BaseModel):
    """Admin dashboard statistics."""
    total_users: int
    total_languages: int
    total_sections: int
    total_videos: int
    total_practice_problems: int
    total_discussions: int
    active_learning_paths: int
    recent_registrations: int


# ============================================================================
# Admin Dashboard & Stats
# ============================================================================

@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Get comprehensive admin dashboard statistics.
    
    **Admin only** - Provides overview of platform metrics.
    """
    from app.models.learning_path import LearningPath
    from app.models.discussion import Discussion
    
    # Get counts
    total_users = await db.scalar(select(func.count()).select_from(User))
    total_languages = await db.scalar(select(func.count()).select_from(Language))
    total_sections = await db.scalar(select(func.count()).select_from(DocSection))
    total_videos = await db.scalar(select(func.count()).select_from(VideoResource))
    total_practice = await db.scalar(select(func.count()).select_from(PracticeProblem))
    total_discussions = await db.scalar(select(func.count()).select_from(Discussion))
    
    # Active paths (not completed)
    active_paths = await db.scalar(
        select(func.count())
        .select_from(LearningPath)
        .where(LearningPath.completed_at.is_(None))
    )
    
    # Recent registrations (last 7 days)
    from datetime import timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = await db.scalar(
        select(func.count())
        .select_from(User)
        .where(User.created_at >= seven_days_ago)
    )
    
    logger.info(f"Admin {admin.email} accessed dashboard stats")
    
    return AdminStatsResponse(
        total_users=total_users or 0,
        total_languages=total_languages or 0,
        total_sections=total_sections or 0,
        total_videos=total_videos or 0,
        total_practice_problems=total_practice or 0,
        total_discussions=total_discussions or 0,
        active_learning_paths=active_paths or 0,
        recent_registrations=recent_users or 0
    )


# ============================================================================
# Language Management
# ============================================================================

@router.post("/languages", status_code=status.HTTP_201_CREATED)
async def create_language(
    language_data: LanguageCreateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Create a new programming language.
    
    **Admin only** - Adds a new language to the platform.
    """
    # Check if slug already exists
    existing = await db.scalar(
        select(Language).where(Language.slug == language_data.slug)
    )
    if existing:
        raise BadRequestException(
            message="Language with this slug already exists",
            details={"slug": language_data.slug}
        )
    
    language = Language(**language_data.model_dump())
    db.add(language)
    await db.commit()
    await db.refresh(language)
    
    logger.info(f"Admin {admin.email} created language: {language.name}")
    
    return language


@router.put("/languages/{language_id}")
async def update_language(
    language_id: UUID,
    update_data: LanguageUpdateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Update a language."""
    language = await db.get(Language, language_id)
    if not language:
        raise NotFoundException(message="Language not found")
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(language, field, value)
    
    await db.commit()
    await db.refresh(language)
    
    logger.info(f"Admin {admin.email} updated language: {language.name}")
    
    return language


@router.delete("/languages/{language_id}")
async def delete_language(
    language_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Delete a language (soft delete by setting is_active=False)."""
    language = await db.get(Language, language_id)
    if not language:
        raise NotFoundException(message="Language not found")
    
    language.is_active = False
    await db.commit()
    
    logger.info(f"Admin {admin.email} deactivated language: {language.name}")
    
    return SuccessResponse(
        message="Language deactivated successfully",
        data={"language_id": str(language_id)}
    )


# ============================================================================
# Documentation Section Management
# ============================================================================

@router.post("/sections", status_code=status.HTTP_201_CREATED)
async def create_doc_section(
    section_data: DocSectionCreateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Create a new documentation section.
    
    **Admin only** - Adds scraped or manual documentation content.
    """
    # Verify language exists
    language = await db.get(Language, section_data.language_id)
    if not language:
        raise NotFoundException(message="Language not found")
    
    section = DocSection(**section_data.model_dump())
    db.add(section)
    await db.commit()
    await db.refresh(section)
    
    logger.info(f"Admin {admin.email} created section: {section.title}")
    
    return section


@router.put("/sections/{section_id}")
async def update_doc_section(
    section_id: UUID,
    update_data: DocSectionUpdateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Update a documentation section."""
    section = await db.get(DocSection, section_id)
    if not section:
        raise NotFoundException(message="Section not found")
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(section, field, value)
    
    await db.commit()
    await db.refresh(section)
    
    logger.info(f"Admin {admin.email} updated section: {section.title}")
    
    return section


@router.delete("/sections/{section_id}")
async def delete_doc_section(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Delete a documentation section."""
    section = await db.get(DocSection, section_id)
    if not section:
        raise NotFoundException(message="Section not found")
    
    await db.delete(section)
    await db.commit()
    
    logger.info(f"Admin {admin.email} deleted section: {section.title}")
    
    return SuccessResponse(
        message="Section deleted successfully",
        data={"section_id": str(section_id)}
    )


# ============================================================================
# Video Resource Management
# ============================================================================

@router.post("/videos", status_code=status.HTTP_201_CREATED)
async def add_video_resource(
    video_data: VideoResourceCreateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Add a curated video resource to a section."""
    # Verify section exists
    section = await db.get(DocSection, video_data.doc_section_id)
    if not section:
        raise NotFoundException(message="Section not found")
    
    video = VideoResource(**video_data.model_dump())
    db.add(video)
    await db.commit()
    await db.refresh(video)
    
    logger.info(f"Admin {admin.email} added video: {video.title}")
    
    return video


@router.delete("/videos/{video_id}")
async def delete_video_resource(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Remove a video resource."""
    video = await db.get(VideoResource, video_id)
    if not video:
        raise NotFoundException(message="Video not found")
    
    await db.delete(video)
    await db.commit()
    
    logger.info(f"Admin {admin.email} deleted video: {video.title}")
    
    return SuccessResponse(
        message="Video deleted successfully",
        data={"video_id": str(video_id)}
    )


# ============================================================================
# Practice Problem Management
# ============================================================================

@router.post("/practice-problems", status_code=status.HTTP_201_CREATED)
async def add_practice_problem(
    problem_data: PracticeProblemCreateAdmin,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Add a curated practice problem to a section."""
    # Verify section exists
    section = await db.get(DocSection, problem_data.doc_section_id)
    if not section:
        raise NotFoundException(message="Section not found")
    
    problem = PracticeProblem(**problem_data.model_dump())
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    
    logger.info(f"Admin {admin.email} added practice problem: {problem.title}")
    
    return problem


@router.delete("/practice-problems/{problem_id}")
async def delete_practice_problem(
    problem_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Remove a practice problem."""
    problem = await db.get(PracticeProblem, problem_id)
    if not problem:
        raise NotFoundException(message="Practice problem not found")
    
    await db.delete(problem)
    await db.commit()
    
    logger.info(f"Admin {admin.email} deleted practice problem: {problem.title}")
    
    return SuccessResponse(
        message="Practice problem deleted successfully",
        data={"problem_id": str(problem_id)}
    )


# ============================================================================
# User Management
# ============================================================================

@router.get("/users")
async def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """List all users (paginated)."""
    result = await db.execute(
        select(User)
        .order_by(desc(User.created_at))
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    
    return [
        {
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "full_name": u.full_name,
            "is_admin": u.is_admin,
            "is_premium": u.is_premium,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]


@router.post("/users/promote")
async def promote_user_to_admin(
    request: UserPromoteRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Promote a user to admin status."""
    user = await db.get(User, request.user_id)
    if not user:
        raise NotFoundException(message="User not found")
    
    user.is_admin = True
    await db.commit()
    
    logger.info(f"Admin {admin.email} promoted user {user.email} to admin")
    
    return SuccessResponse(
        message=f"User {user.email} promoted to admin",
        data={"user_id": str(user.id), "email": user.email}
    )

# ============================================================================
# SCRAPING ENDPOINTS
# ============================================================================
class ScrapeLanguageRequest(BaseModel):
    """Request to scrape a language's documentation."""
    language_name: str
    official_doc_url: HttpUrl
    add_videos: bool = False


class ScrapeResponse(BaseModel):
    """Response from scraping operation."""
    success: bool
    language_id: Optional[str] = None
    language_name: str
    sections_scraped: int = 0
    sections_stored: int = 0
    videos_added: int = 0
    errors: List[str] = []


@router.post("/scrape/language", response_model=ScrapeResponse)
async def scrape_language_documentation(
    request: ScrapeLanguageRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Scrape and store documentation for a programming language.
    
    **Admin only** - Initiates web scraping of official documentation.
    
    Supports:
    - Python (via docs.python.org)
    - More scrapers coming soon
    
    Process:
    1. Scrapes documentation structure
    2. Extracts content from each section
    3. Generates AI summaries
    4. Stores in database
    5. Optionally adds curated YouTube videos
    """
    errors = []
    
    try:
        # Scrape and store documentation
        result = await scraper_service.scrape_and_store_language(
            db=db,
            language_name=request.language_name,
            official_doc_url=str(request.official_doc_url)
        )
        
        videos_added = 0
        
        # Add videos if requested
        if request.add_videos and result.get("language_id"):
            try:
                from uuid import UUID
                videos_added = await scraper_service.add_videos_to_sections(
                    db=db,
                    language_id=UUID(result["language_id"]),
                    max_videos_per_section=3
                )
            except Exception as e:
                errors.append(f"Video scraping failed: {str(e)}")
                logger.error(f"Video scraping error: {e}")
        
        logger.info(
            f"Admin {admin.email} scraped {request.language_name}: "
            f"{result['sections_stored']} sections, {videos_added} videos"
        )
        
        return ScrapeResponse(
            success=True,
            language_id=result.get("language_id"),
            language_name=result["language_name"],
            sections_scraped=result["sections_scraped"],
            sections_stored=result["sections_stored"],
            videos_added=videos_added,
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return ScrapeResponse(
            success=False,
            language_name=request.language_name,
            errors=[str(e)]
        )


@router.post("/scrape/videos/{language_id}")
async def add_videos_to_language(
    language_id: UUID,
    max_per_section: int = Query(3, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Add curated YouTube videos to all sections of a language.
    
    **Admin only** - Searches YouTube for relevant tutorials.
    """
    # Verify language exists
    language = await db.get(Language, language_id)
    if not language:
        raise NotFoundException(message="Language not found")
    
    try:
        videos_added = await scraper_service.add_videos_to_sections(
            db=db,
            language_id=language_id,
            max_videos_per_section=max_per_section
        )
        
        logger.info(f"Admin {admin.email} added {videos_added} videos to {language.name}")
        
        return SuccessResponse(
            message=f"Added {videos_added} videos to {language.name}",
            data={
                "language_id": str(language_id),
                "videos_added": videos_added
            }
        )
    except Exception as e:
        logger.error(f"Video addition failed: {e}")
        raise BadRequestException(
            message="Failed to add videos",
            details={"error": str(e)}
        )


@router.get("/scrape/status")
async def get_scraping_status(
    admin: User = Depends(get_current_admin_user)
):
    """
    Get status of available scrapers.
    
    **Admin only** - Shows which scrapers are configured and ready.
    """
    from app.core.config import settings
    
    status = {
        "scrapers": {
            "python": {
                "available": True,
                "description": "Python official documentation (docs.python.org)"
            },
            "javascript": {
                "available": False,
                "description": "Coming soon"
            }
        },
        "integrations": {
            "youtube": {
                "configured": bool(settings.YOUTUBE_API_KEY),
                "description": "YouTube video search"
            },
            "leetcode": {
                "configured": False,
                "description": "Coming soon"
            }
        },
        "ai": {
            "groq": {
                "configured": bool(settings.GROQ_API_KEY),
                "model": settings.GROQ_MODEL
            },
            "claude": {
                "configured": bool(settings.ANTHROPIC_API_KEY),
                "model": settings.CLAUDE_MODEL if settings.ANTHROPIC_API_KEY else None
            }
        }
    }
    
    return status

@router.post("/scrape/problems/{language_id}")
async def add_problems_to_language(
    language_id: UUID,
    max_per_section: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    Add curated practice problems to all sections of a language.
    
    **Admin only** - Maps LeetCode problems to documentation topics.
    """
    # Verify language exists
    language = await db.get(Language, language_id)
    if not language:
        raise NotFoundException(message="Language not found")
    
    try:
        problems_added = await scraper_service.add_problems_to_sections(
            db=db,
            language_id=language_id,
            max_problems_per_section=max_per_section
        )
        
        logger.info(f"Admin {admin.email} added {problems_added} problems to {language.name}")
        
        return SuccessResponse(
            message=f"Added {problems_added} practice problems to {language.name}",
            data={
                "language_id": str(language_id),
                "problems_added": problems_added
            }
        )
    except Exception as e:
        logger.error(f"Problem addition failed: {e}")
        raise BadRequestException(
            message="Failed to add problems",
            details={"error": str(e)}
        )
