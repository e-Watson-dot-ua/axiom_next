from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from .config import settings


# Create async engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    # Use NullPool for testing to avoid connection issues
    poolclass=NullPool if settings.DEBUG else None,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def create_db_and_tables():
    # Create database tables based on SQLModel metadata
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # Dependency function that yields database sessions
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_context() -> AsyncSession:
    # Get a database session for use outside of FastAPI dependency injection
    return AsyncSessionLocal()


# Health check function
async def check_database_health() -> bool:
    # Check if database connection is healthy
    try:
        async with engine.begin() as conn:
            await conn.exec_driver_sql("SELECT 1")
        return True
    except Exception:
        return False


# Utility functions for database operations
async def close_db():
    # Close database connections gracefully
    await engine.dispose()
    print("✅ Database connections closed")


# Database context manager for transactions
class DatabaseTransaction:
    # Context manager for database transactions
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()