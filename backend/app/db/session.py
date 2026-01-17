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
_engine_kwargs = {
    "echo": settings.DATABASE_ECHO,
    "future": True,
    "pool_pre_ping": True,  # Verify connections before using
}

if settings.is_development:
    _engine_kwargs["poolclass"] = NullPool
else:
    _engine_kwargs["poolclass"] = QueuePool
    _engine_kwargs["pool_size"] = 10  # Max connections in pool
    _engine_kwargs["max_overflow"] = 20  # Max overflow connections
    _engine_kwargs["pool_recycle"] = 3600  # Recycle connections after 1 hour

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

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
    # Import all models to register them with SQLAlchemy
    from app.models import (
        Base, User, Language, DocSection, CodeExample,
        LearningPath, UserProgress, PracticeProblem,
        VideoResource, Bookmark, UserNote, Discussion,
        DiscussionComment
    )
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized successfully")


async def close_db():
    """Close database connection pool."""
    await engine.dispose()
    logger.info("Database connection closed")