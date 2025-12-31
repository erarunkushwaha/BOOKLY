"""
Database configuration and session management module.

This module handles:
- Database engine creation with connection pooling
- Async session factory setup
- Database initialization (table creation)
- FastAPI dependency for database sessions
"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool, QueuePool
from sqlmodel import SQLModel
from typing import AsyncGenerator
import logging

from src.config import Config

# Configure logging for database operations
logger = logging.getLogger(__name__)


# Create async database engine with connection pooling
# This engine manages the connection pool and provides async database access
engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,  # Database connection URL from config
    echo=Config.DB_ECHO,  # Log SQL queries if enabled in config
    pool_size=Config.DB_POOL_SIZE,  # Number of connections in the pool
    max_overflow=Config.DB_MAX_OVERFLOW,  # Max connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before using them (prevents stale connections)
    pool_recycle=3600,  # Recycle connections after 1 hour (prevents connection timeouts)
    future=True,  # Use SQLAlchemy 2.0 style
)


# Create async session factory
# This factory creates new database sessions for each request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # Use the engine we created above
    class_=AsyncSession,  # Use async session class
    expire_on_commit=False,  # Don't expire objects after commit (allows access after commit)
    autoflush=False,  # Don't auto-flush (we'll do it manually for better control)
    autocommit=False,  # Use explicit transactions
)


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function should be called once when the application starts.
    It creates all tables defined in SQLModel models based on their metadata.
    
    Note: In production, you might want to use Alembic migrations instead
    of creating tables automatically.
    
    Raises:
        Exception: If database connection or table creation fails
    """
    try:
        logger.info("Initializing database...")
        
        # Begin a transaction to create tables
        async with engine.begin() as conn:
            # Import all models to ensure their metadata is registered
            from src.books.models import Book
            
            # Create all tables defined in SQLModel metadata
            # This uses the sync method but runs it in an async context
            await conn.run_sync(SQLModel.metadata.create_all)
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db() -> None:
    """
    Close all database connections and dispose of the engine.
    
    This function should be called when the application shuts down
    to properly clean up database connections.
    """
    try:
        logger.info("Closing database connections...")
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency function that provides a database session.
    
    This is a dependency injection function that FastAPI will call
    for each request that needs database access. It creates a new
    session, yields it to the route handler, and then closes it
    after the request is complete (even if an error occurs).
    
    Usage in routes:
        @router.get("/books")
        async def get_books(session: AsyncSession = Depends(get_session)):
            # Use session here
            pass
    
    Yields:
        AsyncSession: A database session that can be used for queries
        
    Note:
        The session is automatically closed after the request completes
        thanks to the async generator pattern.
    """
    # Create a new session from the factory
    async with AsyncSessionLocal() as session:
        try:
            # Yield the session to the route handler
            yield session
            # Commit the transaction if no exception occurred
            await session.commit()
        except Exception:
            # Rollback the transaction if an error occurred
            await session.rollback()
            # Re-raise the exception so FastAPI can handle it
            raise
        finally:
            # Always close the session (this is done automatically by async with)
            # but we include it here for clarity
            await session.close()