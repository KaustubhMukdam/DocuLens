"""
Database session management and connection pool configuration.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings
from app.core.logging import logger


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,  # Verify connections before using
    poolclass=QueuePool if not settings.is_development else NullPool,
    pool_size=10,  # Max connections in pool
    max_overflow=20,  # Max overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    
    Yields:
        AsyncSession: Database session
        
    Example:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database - create all tables."""
    from app.models.base import Base
    
    # Import all models here to ensure they're registered
    from app.models.user import User
    from app.models.language import Language
    from app.models.doc_section import DocSection
    from app.models.code_example import CodeExample
    from app.models.learning_path import LearningPath
    from app.models.user_progress import UserProgress
    from app.models.practice_problem import PracticeProblem
    from app.models.video_resource import VideoResource
    from app.models.bookmark import Bookmark
    from app.models.user_note import UserNote
    from app.models.discussion import Discussion
    from app.models.discussion_comment import DiscussionComment
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized successfully")


async def close_db():
    """Close database connection pool."""
    await engine.dispose()
    logger.info("Database connection closed")