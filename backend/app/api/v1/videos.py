# ============================================================================
# app/api/v1/videos.py
# ============================================================================
"""Video resource endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, HttpUrl

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.crud.video_resource import video_resource_crud, VideoResourceCreate, VideoResourceUpdate
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.schemas.response import SuccessResponse
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
    duration_seconds: Optional[int]
    channel_name: Optional[str]
    thumbnail_url: Optional[str]
    description: Optional[str]
    order_index: int
    
    class Config:
        from_attributes = True


class YouTubeSearchResult(BaseModel):
    """YouTube search result schema."""
    title: str
    video_id: str
    url: str
    thumbnail_url: str
    channel_name: str
    duration: Optional[str] = None
    view_count: Optional[int] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/sections/{section_id}", response_model=List[VideoResourceResponse])
async def get_section_videos(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all video resources for a documentation section.
    
    Returns curated video tutorials and explanations related to the section content.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    videos = await video_resource_crud.get_by_section(db, section_id=section_id)
    
    return [VideoResourceResponse.model_validate(v) for v in videos]


@router.get("/languages/{language_id}", response_model=List[VideoResourceResponse])
async def get_language_videos(
    language_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all video resources for a programming language.
    
    Returns videos across all sections of the language.
    """
    from app.crud.language import CRUDLanguage
    from app.models.language import Language
    
    language_crud = CRUDLanguage(Language)
    
    # Verify language exists
    language = await language_crud.get(db, id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    
    videos = await video_resource_crud.get_by_language(
        db,
        language_id=language_id,
        skip=skip,
        limit=limit
    )
    
    return [VideoResourceResponse.model_validate(v) for v in videos]


@router.post("/sections/{section_id}", response_model=VideoResourceResponse, status_code=status.HTTP_201_CREATED)
async def add_video_to_section(
    section_id: UUID,
    video_data: VideoResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a video resource to a section.
    
    **Admin/Contributor feature** - Add authorization check as needed.
    
    Allows curators to add helpful video tutorials to documentation sections.
    """
    # TODO: Add admin/contributor check
    # if not current_user.is_admin and not current_user.is_contributor:
    #     raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Override section_id in case it differs
    video_data.doc_section_id = section_id
    
    # Create video resource
    video = await video_resource_crud.create(db, obj_in=video_data)
    await db.commit()
    await db.refresh(video)
    
    logger.info(f"User {current_user.id} added video {video.id} to section {section_id}")
    
    return VideoResourceResponse.model_validate(video)


@router.put("/{video_id}", response_model=VideoResourceResponse)
async def update_video(
    video_id: UUID,
    update_data: VideoResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a video resource.
    
    **Admin/Contributor feature** - Add authorization check as needed.
    """
    # TODO: Add admin/contributor check
    
    video = await video_resource_crud.get(db, id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    updated_video = await video_resource_crud.update(db, db_obj=video, obj_in=update_data)
    await db.commit()
    await db.refresh(updated_video)
    
    logger.info(f"Video {video_id} updated by user {current_user.id}")
    
    return VideoResourceResponse.model_validate(updated_video)


@router.delete("/{video_id}", response_model=SuccessResponse)
async def delete_video(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a video resource.
    
    **Admin/Contributor feature** - Add authorization check as needed.
    """
    # TODO: Add admin/contributor check
    
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


@router.post("/search/youtube", response_model=List[YouTubeSearchResult])
async def search_youtube_videos(
    query: str = Query(..., min_length=3, max_length=200),
    max_results: int = Query(10, ge=1, le=20),
    current_user: User = Depends(get_current_user)
):
    """
    Search YouTube for relevant tutorial videos.
    
    **Premium feature** - Helps users discover quality learning content.
    
    Note: Requires YouTube Data API key to be configured.
    Returns mock data if API key not available.
    """
    # TODO: Implement YouTube API integration
    # For now, return mock data
    
    logger.info(f"User {current_user.id} searched YouTube for: {query}")
    
    # Mock response
    mock_results = [
        YouTubeSearchResult(
            title=f"{query} - Complete Tutorial",
            video_id="mock_id_1",
            url="https://youtube.com/watch?v=mock_id_1",
            thumbnail_url="https://i.ytimg.com/vi/mock_id_1/default.jpg",
            channel_name="Programming Tutorials",
            duration="15:30",
            view_count=125000
        ),
        YouTubeSearchResult(
            title=f"Learn {query} in 30 Minutes",
            video_id="mock_id_2",
            url="https://youtube.com/watch?v=mock_id_2",
            thumbnail_url="https://i.ytimg.com/vi/mock_id_2/default.jpg",
            channel_name="Code Academy",
            duration="28:45",
            view_count=89000
        )
    ]
    
    return mock_results[:max_results]
