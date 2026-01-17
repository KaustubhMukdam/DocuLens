from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from datetime import datetime

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.core.exceptions import UnauthorizedException

class AuthService:
    async def get_current_user(self, db: AsyncSession, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise UnauthorizedException("Could not validate credentials")
        except JWTError:
            raise UnauthorizedException("Could not validate credentials")
            
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalars().first()
        
        if user is None:
            raise UnauthorizedException("User not found")
        return user

auth_service = AuthService()