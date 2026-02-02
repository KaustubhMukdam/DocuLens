# ============================================================================
# app/api/v1/bookmarks.py
# ============================================================================
"""Bookmark endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.bookmark import Bookmark
from app.schemas.language import BookmarkCreate, BookmarkUpdate, BookmarkResponse
from app.schemas.response import SuccessResponse
from app.crud.bookmark import bookmark_crud
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.core.logging import logger

router = APIRouter()

doc_section_crud = CRUDDocSection(DocSection)


@router.post("", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    bookmark_data: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a bookmark for a documentation section.
    
    Bookmarks allow users to save sections for quick access later.
    Optional notes can be added to remember why it was bookmarked.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=bookmark_data.doc_section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Create bookmark
    bookmark = await bookmark_crud.create_bookmark(
        db,
        user_id=current_user.id,
        section_id=bookmark_data.doc_section_id,
        notes=bookmark_data.notes
    )
    
    await db.commit()
    await db.refresh(bookmark)
    
    # Load relationships for response
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    
    result = await db.execute(
        select(bookmark.__class__)
        .where(bookmark.__class__.id == bookmark.id)
        .options(
            selectinload(bookmark.__class__.doc_section).selectinload(DocSection.language)
        )
    )
    bookmark_with_relations = result.scalar_one()
    
    logger.info(f"User {current_user.id} bookmarked section {bookmark_data.doc_section_id}")
    
    # Build response with related data
    response = BookmarkResponse.model_validate(bookmark_with_relations)
    if bookmark_with_relations.doc_section:
        response.section_title = bookmark_with_relations.doc_section.title
        response.section_slug = bookmark_with_relations.doc_section.slug
        if bookmark_with_relations.doc_section.language:
            response.language_name = bookmark_with_relations.doc_section.language.name
    
    return response


@router.get("", response_model=List[BookmarkResponse])
async def get_my_bookmarks(
    language_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all bookmarks for the current user."""
    try:
        # Build query with eager loading to avoid lazy loading issues
        query = (
            select(Bookmark)
            .options(
                selectinload(Bookmark.doc_section).selectinload(DocSection.language)
            )
            .filter(Bookmark.user_id == current_user.id)
            .order_by(Bookmark.created_at.desc())
        )
        
        if language_id:
            query = query.join(DocSection).filter(DocSection.language_id == language_id)
        
        result = await db.execute(query)
        bookmarks = result.scalars().all()
        
        # Convert to response format
        response_data = []
        for bookmark in bookmarks:
            response_data.append({
                "id": bookmark.id,
                "user_id": bookmark.user_id,  # ADD THIS LINE
                "doc_section_id": bookmark.doc_section_id,
                "notes": bookmark.notes,
                "created_at": bookmark.created_at,
                "section_title": bookmark.doc_section.title if bookmark.doc_section else "Unknown Section",
                "language_name": bookmark.doc_section.language.name if bookmark.doc_section and bookmark.doc_section.language else "Unknown Language"
            })
        
        return response_data
    except Exception as e:
        logger.error(f"Error fetching bookmarks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bookmark_id}", response_model=BookmarkResponse)
async def get_bookmark(
    bookmark_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific bookmark by ID."""
    bookmark = await bookmark_crud.get(db, id=bookmark_id)
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    if bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this bookmark"
        )
    
    # Load relationships
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    
    result = await db.execute(
        select(bookmark.__class__)
        .where(bookmark.__class__.id == bookmark.id)
        .options(
            selectinload(bookmark.__class__.doc_section).selectinload(DocSection.language)
        )
    )
    bookmark_with_relations = result.scalar_one()
    
    response = BookmarkResponse.model_validate(bookmark_with_relations)
    if bookmark_with_relations.doc_section:
        response.section_title = bookmark_with_relations.doc_section.title
        response.section_slug = bookmark_with_relations.doc_section.slug
        if bookmark_with_relations.doc_section.language:
            response.language_name = bookmark_with_relations.doc_section.language.name
    
    return response


@router.put("/{bookmark_id}", response_model=BookmarkResponse)
async def update_bookmark(
    bookmark_id: UUID,
    update_data: BookmarkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update bookmark notes.
    
    Only notes can be updated. To bookmark a different section, delete and create new.
    """
    bookmark = await bookmark_crud.get(db, id=bookmark_id)
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    if bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this bookmark"
        )
    
    # Update
    updated_bookmark = await bookmark_crud.update(db, db_obj=bookmark, obj_in=update_data)
    await db.commit()
    await db.refresh(updated_bookmark)
    
    logger.info(f"Bookmark {bookmark_id} updated by user {current_user.id}")
    
    return BookmarkResponse.model_validate(updated_bookmark)


@router.delete("/{bookmark_id}", response_model=SuccessResponse)
async def delete_bookmark(
    bookmark_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a bookmark."""
    bookmark = await bookmark_crud.get(db, id=bookmark_id)
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    if bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this bookmark"
        )
    
    await bookmark_crud.delete(db, id=bookmark_id)
    await db.commit()
    
    logger.info(f"Bookmark {bookmark_id} deleted by user {current_user.id}")
    
    return SuccessResponse(
        message="Bookmark deleted successfully",
        data={"bookmark_id": str(bookmark_id)}
    )


@router.delete("/section/{section_id}", response_model=SuccessResponse)
async def delete_bookmark_by_section(
    section_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete bookmark by section ID.
    
    Convenient endpoint for toggling bookmarks.
    """
    deleted = await bookmark_crud.delete_bookmark(
        db,
        user_id=current_user.id,
        section_id=section_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    await db.commit()
    
    logger.info(f"User {current_user.id} removed bookmark for section {section_id}")
    
    return SuccessResponse(
        message="Bookmark removed successfully",
        data={"section_id": str(section_id)}
    )
