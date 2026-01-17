# ============================================================================
# app/api/v1/users.py
# ============================================================================
"""User endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse
from app.schemas.response import SuccessResponse
from app.crud import user as user_crud
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information."""
    updated_user = await user_crud.update(
        db=db,
        db_obj=current_user,
        obj_in=user_update
    )
    await db.commit()
    return UserResponse.model_validate(updated_user)


@router.delete("/me", response_model=SuccessResponse)
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete current user account."""
    await user_crud.delete(db=db, id=current_user.id)
    await db.commit()
    return SuccessResponse(
        success=True,
        message="Account deleted successfully"
    )


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed user profile with statistics."""
    # TODO: Calculate statistics from learning paths and progress
    profile = UserProfileResponse.model_validate(current_user)
    profile.total_learning_paths = 0
    profile.completed_paths = 0
    profile.total_sections_completed = 0
    profile.total_time_spent_minutes = 0
    profile.current_streak_days = 0
    return profile