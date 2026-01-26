# ============================================================================
# app/api/v1/videos.py - UPDATED WITH FULL YOUTUBE INTEGRATION
# ============================================================================
"""Video resource endpoints with YouTube API integration."""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from app.api.deps import get_db, get_current_user, get_optional_current_user
from app.models.user import User
from app.models.video_resource import VideoResource
from app.crud.video_resource import video_resource_crud, VideoResourceCreate, VideoResourceUpdate
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.schemas.response import SuccessResponse
from app.scrapers.youtube import YouTubeIntegration, search_tutorial_videos
from app.core.logging import logger

router = APIRouter()
doc_section_crud = CRUDDocSection(DocSection)

# ============================================================================
# Schemas
# ============================================================================

class VideoResourceResponse(BaseModel):
    """Video resource response schema."""
    id: UUID
    doc_section_id: UUID
    title: str
    url: str
    platform: str
    duration_seconds: Optional[int] = None
    channel_name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
    order_index: int
    
    class Config:
        from_attributes = True


class YouTubeSearchResult(BaseModel):
    """YouTube search result schema."""
    title: str
    video_url: str
    thumbnail_url: Optional[str] = None
    channel_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    views: Optional[int] = None
    platform: str = "youtube"


class VideoScrapeRequest(BaseModel):
    """Request to scrape videos for a section."""
    max_results: int = Field(default=3, ge=1, le=10, description="Maximum number of videos to scrape")
    order: str = Field(default="relevance", description="Sort order: relevance, date, viewCount, rating")


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/sections/{section_id}", response_model=List[VideoResourceResponse])
async def get_section_videos(
    section_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all video resources for a documentation section.
    Public endpoint - no authentication required.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Get videos ordered by order_index
    result = await db.execute(
        select(VideoResource)
        .where(VideoResource.doc_section_id == section_id)
        .order_by(VideoResource.order_index)
    )
    videos = result.scalars().all()
    
    return [VideoResourceResponse.model_validate(v) for v in videos]


@router.post("/sections/{section_id}/scrape", response_model=SuccessResponse)
async def scrape_videos_for_section(
    section_id: UUID,
    scrape_request: VideoScrapeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Scrape and add YouTube videos for a section.
    Uses YouTube Data API to find relevant tutorials.
    """
    # Verify section exists
    section_result = await db.execute(
        select(DocSection)
        .where(DocSection.id == section_id)
    )
    section = section_result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Build search query
    query = f"{section.language.name if hasattr(section, 'language') else 'Programming'} {section.title} tutorial"
    
    logger.info(f"Scraping YouTube videos for section {section_id}: {query}")
    
    try:
        # Search YouTube
        youtube = YouTubeIntegration()
        video_data = await youtube.search_videos(
            query=query,
            max_results=scrape_request.max_results,
            order=scrape_request.order
        )
        
        # Get current max order_index
        max_order_result = await db.execute(
            select(func.max(VideoResource.order_index))
            .where(VideoResource.doc_section_id == section_id)
        )
        max_order = max_order_result.scalar() or -1
        
        # Save videos to database
        saved_videos = []
        for idx, video in enumerate(video_data):
            video_resource = VideoResource(
                doc_section_id=section_id,
                title=video["title"],
                url=video["video_url"],
                platform=video["platform"],
                channel_name=video.get("channel_name"),
                thumbnail_url=video.get("thumbnail_url"),
                duration_seconds=video.get("duration_seconds"),
                description=f"Views: {video.get('views', 'N/A')}",
                order_index=max_order + idx + 1
            )
            db.add(video_resource)
            saved_videos.append(video_resource.title)
        
        await db.commit()
        
        logger.info(f"Successfully scraped {len(video_data)} videos for section {section_id}")
        
        return SuccessResponse(
            message=f"Successfully added {len(video_data)} videos",
            data={
                "section_id": str(section_id),
                "videos_added": len(video_data),
                "titles": saved_videos
            }
        )
        
    except Exception as e:
        logger.error(f"Error scraping videos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to scrape videos: {str(e)}"
        )


@router.post("/search/youtube", response_model=List[YouTubeSearchResult])
async def search_youtube_videos(
    query: str = Query(..., min_length=3, max_length=200),
    max_results: int = Query(10, ge=1, le=20),
    current_user: User = Depends(get_current_user)
):
    """
    Search YouTube for relevant tutorial videos.
    Returns live results from YouTube Data API.
    """
    try:
        youtube = YouTubeIntegration()
        search_query = f"{query} programming tutorial"
        
        results = await youtube.search_videos(
            query=search_query,
            max_results=max_results,
            order="relevance"
        )
        
        return [YouTubeSearchResult(**video) for video in results]
        
    except Exception as e:
        logger.error(f"YouTube search error: {e}")
        # Return empty list instead of error for better UX
        return []


@router.post("/sections/{section_id}", response_model=VideoResourceResponse, status_code=status.HTTP_201_CREATED)
async def add_video_to_section(
    section_id: UUID,
    video_data: VideoResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a video resource manually to a section."""
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    video_data.doc_section_id = section_id
    video = await video_resource_crud.create(db, obj_in=video_data)
    await db.commit()
    await db.refresh(video)
    
    logger.info(f"User {current_user.id} added video {video.id} to section {section_id}")
    return VideoResourceResponse.model_validate(video)


@router.delete("/{video_id}", response_model=SuccessResponse)
async def delete_video(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a video resource."""
    video = await video_resource_crud.get(db, id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    await video_resource_crud.delete(db, id=video_id)
    await db.commit()
    
    logger.info(f"Video {video_id} deleted by user {current_user.id}")
    return SuccessResponse(
        message="Video deleted successfully",
        data={"video_id": str(video_id)}
    )


# Import func for SQL functions
from sqlalchemy import func
