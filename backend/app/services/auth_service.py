"""
Authentication service for user registration, login, and token management.
"""

from typing import Tuple
from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password_reset_token,
    generate_password_reset_token,
)
from app.core.exceptions import (
    UnauthorizedException,
    ConflictException,
    NotFoundException,
    BadRequestException,
)
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.crud.user import CRUDUser


class AuthService:
    """Authentication service."""

    def __init__(self):
        self.user_crud = CRUDUser(User)

    async def register(
        self, db: AsyncSession, user_in: RegisterRequest
    ) -> Tuple[User, TokenResponse]:
        """
        Register a new user.

        Args:
            db: Database session
            user_in: User registration data

        Returns:
            Tuple of (User, TokenResponse)

        Raises:
            ConflictException: If email or username already exists
        """
        # Check if email already exists
        existing_user = await self.user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise ConflictException(
                message="Email already registered",
                details={"email": user_in.email}
            )

        # Check if username already exists
        existing_username = await self.user_crud.get_by_username(
            db, username=user_in.username
        )
        if existing_username:
            raise ConflictException(
                message="Username already taken",
                details={"username": user_in.username}
            )

        # Create user
        user = await self.user_crud.create(db, obj_in=user_in)
        await db.commit()
        await db.refresh(user)

        # Generate tokens
        tokens = self._create_user_tokens(user)

        return user, tokens

    async def login(
        self, db: AsyncSession, credentials: LoginRequest
    ) -> Tuple[User, TokenResponse]:
        """
        Authenticate user and return tokens.

        Args:
            db: Database session
            credentials: Login credentials

        Returns:
            Tuple of (User, TokenResponse)

        Raises:
            UnauthorizedException: If credentials are invalid
        """
        # Authenticate user
        user = await self.user_crud.authenticate(
            db, email=credentials.email, password=credentials.password
        )

        if not user:
            raise UnauthorizedException(
                message="Incorrect email or password",
            )

        if not user.is_active:
            raise UnauthorizedException(
                message="Account is inactive",
            )

        # Update last login
        from datetime import datetime
        user.last_login = datetime.utcnow()
        await db.commit()

        # Generate tokens
        tokens = self._create_user_tokens(user)

        return user, tokens

    async def refresh_token(
        self, db: AsyncSession, refresh_token: str
    ) -> TokenResponse:
        """
        Refresh access token using refresh token.

        Args:
            db: Database session
            refresh_token: Refresh token

        Returns:
            New token response

        Raises:
            UnauthorizedException: If refresh token is invalid
        """
        # Decode refresh token
        payload = decode_token(refresh_token)

        if not payload:
            raise UnauthorizedException(message="Invalid refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedException(message="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException(message="Invalid token payload")

        # Get user
        try:
            user = await self.user_crud.get(db, id=UUID(user_id))
        except ValueError:
            raise UnauthorizedException(message="Invalid user ID in token")

        if not user:
            raise UnauthorizedException(message="User not found")

        if not user.is_active:
            raise UnauthorizedException(message="Account is inactive")

        # Generate new tokens
        return self._create_user_tokens(user)

    async def get_current_user(self, db: AsyncSession, token: str) -> User:
        """
        Get current user from access token.

        Args:
            db: Database session
            token: Access token

        Returns:
            User object

        Raises:
            UnauthorizedException: If token is invalid or user not found
        """
        # Decode token
        payload = decode_token(token)

        if not payload:
            raise UnauthorizedException(message="Could not validate credentials")

        if payload.get("type") != "access":
            raise UnauthorizedException(message="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException(message="Invalid token payload")

        # Get user
        try:
            user = await self.user_crud.get(db, id=UUID(user_id))
        except ValueError:
            raise UnauthorizedException(message="Invalid user ID in token")

        if not user:
            raise UnauthorizedException(message="User not found")

        return user

    async def request_password_reset(self, db: AsyncSession, email: str) -> str:
        """
        Generate password reset token for user.

        Args:
            db: Database session
            email: User email

        Returns:
            Password reset token

        Raises:
            NotFoundException: If user not found (in production, return success anyway)
        """
        # Get user by email
        user = await self.user_crud.get_by_email(db, email=email)

        # In production, always return success to prevent user enumeration
        # For now, we'll raise an exception for development
        if not user:
            # TODO: In production, still return success but don't send email
            raise NotFoundException(message="User with this email not found")

        # Generate reset token
        token = generate_password_reset_token(email)

        return token

    async def reset_password(
        self, db: AsyncSession, token: str, new_password: str
    ) -> User:
        """
        Reset user password using reset token.

        Args:
            db: Database session
            token: Password reset token
            new_password: New password

        Returns:
            Updated user

        Raises:
            UnauthorizedException: If token is invalid
            NotFoundException: If user not found
        """
        # Verify token
        email = verify_password_reset_token(token)

        if not email:
            raise UnauthorizedException(message="Invalid or expired reset token")

        # Get user
        user = await self.user_crud.get_by_email(db, email=email)

        if not user:
            raise NotFoundException(message="User not found")

        # Update password
        user.password_hash = get_password_hash(new_password)
        await db.commit()
        await db.refresh(user)

        return user

    def _create_user_tokens(self, user: User) -> TokenResponse:
        """
        Create access and refresh tokens for user.

        Args:
            user: User object

        Returns:
            TokenResponse with access and refresh tokens
        """
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires,
        )

        # Create refresh token
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )


# Global service instance
auth_service = AuthService()