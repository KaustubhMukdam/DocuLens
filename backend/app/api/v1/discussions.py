# ============================================================================
# app/api/v1/discussions.py
# ============================================================================
"""Discussion and comment endpoints."""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.crud.discussion import (
    discussion_crud,
    comment_crud,
    DiscussionCreate,
    DiscussionUpdate,
    CommentCreate,
    CommentUpdate
)
from app.crud.doc_section import CRUDDocSection
from app.models.doc_section import DocSection
from app.schemas.response import SuccessResponse
from app.core.logging import logger

router = APIRouter()

doc_section_crud = CRUDDocSection(DocSection)


# ============================================================================
# Schemas
# ============================================================================

class UserInfo(BaseModel):
    """Basic user info for responses."""
    id: UUID
    username: str
    full_name: Optional[str]
    
    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    """Comment response schema."""
    id: UUID
    discussion_id: UUID
    user_id: UUID
    user: UserInfo
    content: str
    parent_comment_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DiscussionResponse(BaseModel):
    """Discussion response schema."""
    id: UUID
    doc_section_id: UUID
    user_id: UUID
    user: UserInfo
    title: str
    content: str
    is_resolved: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DiscussionDetailResponse(DiscussionResponse):
    """Detailed discussion with comments."""
    comments: List[CommentResponse] = []


# ============================================================================
# Discussion Endpoints
# ============================================================================

@router.post("", response_model=DiscussionResponse, status_code=status.HTTP_201_CREATED)
async def create_discussion(
    discussion_data: DiscussionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new discussion thread for a documentation section.
    
    Allows users to ask questions, share insights, or discuss concepts
    related to specific documentation sections.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=discussion_data.doc_section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    # Create discussion with user_id
    from app.models.discussion import Discussion
    discussion = Discussion(
        user_id=current_user.id,
        doc_section_id=discussion_data.doc_section_id,
        title=discussion_data.title,
        content=discussion_data.content,
        is_resolved=False
    )
    
    db.add(discussion)
    await db.commit()
    await db.refresh(discussion)
    
    # Load user relationship
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Discussion)
        .where(Discussion.id == discussion.id)
        .options(selectinload(Discussion.user))
    )
    discussion_with_user = result.scalar_one()
    
    logger.info(f"User {current_user.id} created discussion {discussion.id}")
    
    return DiscussionResponse.model_validate(discussion_with_user)


@router.get("/sections/{section_id}", response_model=List[DiscussionResponse])
async def get_section_discussions(
    section_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all discussions for a documentation section.
    
    Returns discussions ordered by most recent first.
    """
    # Verify section exists
    section = await doc_section_crud.get(db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    discussions = await discussion_crud.get_by_section(
        db,
        section_id=section_id,
        skip=skip,
        limit=limit
    )
    
    return [DiscussionResponse.model_validate(d) for d in discussions]


@router.get("/me", response_model=List[DiscussionResponse])
async def get_my_discussions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all discussions created by the current user."""
    discussions = await discussion_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return [DiscussionResponse.model_validate(d) for d in discussions]


@router.get("/{discussion_id}", response_model=DiscussionDetailResponse)
async def get_discussion_detail(
    discussion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed discussion with all comments.
    
    Returns the full discussion thread including nested comments.
    """
    discussion = await discussion_crud.get_with_comments(db, discussion_id=discussion_id)
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    return DiscussionDetailResponse.model_validate(discussion)


@router.put("/{discussion_id}", response_model=DiscussionResponse)
async def update_discussion(
    discussion_id: UUID,
    update_data: DiscussionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a discussion.
    
    Only the discussion creator can update it.
    Can mark as resolved when the question is answered.
    """
    discussion = await discussion_crud.get(db, id=discussion_id)
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    # Verify ownership
    if discussion.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this discussion"
        )
    
    updated_discussion = await discussion_crud.update(db, db_obj=discussion, obj_in=update_data)
    await db.commit()
    await db.refresh(updated_discussion)
    
    # Load user
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(discussion.__class__)
        .where(discussion.__class__.id == updated_discussion.id)
        .options(selectinload(discussion.__class__.user))
    )
    discussion_with_user = result.scalar_one()
    
    logger.info(f"Discussion {discussion_id} updated by user {current_user.id}")
    
    return DiscussionResponse.model_validate(discussion_with_user)


@router.delete("/{discussion_id}", response_model=SuccessResponse)
async def delete_discussion(
    discussion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a discussion.
    
    Only the discussion creator can delete it.
    Deletes all associated comments.
    """
    discussion = await discussion_crud.get(db, id=discussion_id)
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    # Verify ownership (or admin)
    if discussion.user_id != current_user.id:
        # TODO: Allow admins to delete
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this discussion"
        )
    
    await discussion_crud.delete(db, id=discussion_id)
    await db.commit()
    
    logger.info(f"Discussion {discussion_id} deleted by user {current_user.id}")
    
    return SuccessResponse(
        message="Discussion deleted successfully",
        data={"discussion_id": str(discussion_id)}
    )


# ============================================================================
# Comment Endpoints
# ============================================================================

@router.post("/{discussion_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    discussion_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a comment to a discussion.
    
    Supports nested comments via parent_comment_id.
    """
    # Verify discussion exists
    discussion = await discussion_crud.get(db, id=discussion_id)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    # Override discussion_id to match URL
    comment_data.discussion_id = discussion_id
    
    # Verify parent comment if provided
    if comment_data.parent_comment_id:
        parent = await comment_crud.get(db, id=comment_data.parent_comment_id)
        if not parent or parent.discussion_id != discussion_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent comment"
            )
    
    # Create comment
    from app.models.discussion_comment import DiscussionComment
    comment = DiscussionComment(
        discussion_id=discussion_id,
        user_id=current_user.id,
        content=comment_data.content,
        parent_comment_id=comment_data.parent_comment_id
    )
    
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    
    # Load user
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(DiscussionComment)
        .where(DiscussionComment.id == comment.id)
        .options(selectinload(DiscussionComment.user))
    )
    comment_with_user = result.scalar_one()
    
    logger.info(f"User {current_user.id} added comment to discussion {discussion_id}")
    
    return CommentResponse.model_validate(comment_with_user)


@router.get("/{discussion_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    discussion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all comments for a discussion."""
    # Verify discussion exists
    discussion = await discussion_crud.get(db, id=discussion_id)
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    comments = await comment_crud.get_by_discussion(db, discussion_id=discussion_id)
    
    return [CommentResponse.model_validate(c) for c in comments]


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: UUID,
    update_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a comment.
    
    Only the comment author can update it.
    """
    comment = await comment_crud.get(db, id=comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Verify ownership
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    updated_comment = await comment_crud.update(db, db_obj=comment, obj_in=update_data)
    await db.commit()
    await db.refresh(updated_comment)
    
    # Load user
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.discussion_comment import DiscussionComment
    
    result = await db.execute(
        select(DiscussionComment)
        .where(DiscussionComment.id == updated_comment.id)
        .options(selectinload(DiscussionComment.user))
    )
    comment_with_user = result.scalar_one()
    
    logger.info(f"Comment {comment_id} updated by user {current_user.id}")
    
    return CommentResponse.model_validate(comment_with_user)


@router.delete("/comments/{comment_id}", response_model=SuccessResponse)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a comment.
    
    Only the comment author can delete it.
    """
    comment = await comment_crud.get(db, id=comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Verify ownership
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    await comment_crud.delete(db, id=comment_id)
    await db.commit()
    
    logger.info(f"Comment {comment_id} deleted by user {current_user.id}")
    
    return SuccessResponse(
        message="Comment deleted successfully",
        data={"comment_id": str(comment_id)}
    )
