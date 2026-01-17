# ============================================================================
# app/api/v1/auth.py
# ============================================================================
"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest,
)
from app.schemas.user import UserResponse
from app.schemas.response import SuccessResponse
from app.services.auth_service import auth_service
from app.models.user import User
from app.core.security import verify_password, get_password_hash

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    user, tokens = await auth_service.register(db=db, user_in=user_in)
    
    # Return user with tokens in headers
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token."""
    user, tokens = await auth_service.login(db=db, credentials=credentials)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    tokens = await auth_service.refresh_token(
        db=db,
        refresh_token=refresh_data.refresh_token
    )
    return tokens


@router.post("/password-reset/request", response_model=SuccessResponse)
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset email."""
    token = await auth_service.request_password_reset(
        db=db,
        email=request.email
    )
    # TODO: Send email with token
    return SuccessResponse(
        success=True,
        message="Password reset email sent",
        data={"token": token}  # Remove in production
    )


@router.post("/password-reset/confirm", response_model=SuccessResponse)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """Confirm password reset with token."""
    await auth_service.reset_password(
        db=db,
        token=reset_data.token,
        new_password=reset_data.new_password
    )
    return SuccessResponse(
        success=True,
        message="Password reset successful"
    )


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Change password for authenticated user."""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    
    return SuccessResponse(
        success=True,
        message="Password changed successfully"
    )
