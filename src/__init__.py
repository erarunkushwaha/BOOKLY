"""
Main FastAPI application module.

This module creates and configures the FastAPI application instance,
sets up middleware, includes routers, and handles application lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.config import Config
from src.db.main import init_db, close_db
from src.books.routes import book_router
from src.auth.routes import auth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    This function handles startup and shutdown events for the FastAPI application.
    It's called automatically by FastAPI when the application starts and stops.

    On startup:
        - Initialize the database (create tables if they don't exist)

    On shutdown:
        - Close database connections gracefully

    Args:
        app: The FastAPI application instance

    Yields:
        None (control is yielded to the application)
    """
    # Startup: Initialize database
    logger.info("Application startup: Initializing database...")
    try:
        await init_db()
        logger.info("Application startup: Database initialized successfully")
    except Exception as e:
        logger.error(f"Application startup: Failed to initialize database: {e}")
        raise

    # Yield control to the application
    # The application will run until it's shut down
    yield

    # Shutdown: Close database connections
    logger.info("Application shutdown: Closing database connections...")
    try:
        await close_db()
        logger.info("Application shutdown: Database connections closed")
    except Exception as e:
        logger.error(f"Application shutdown: Error closing database: {e}")


# Create FastAPI application instance
# This is the main application object that handles all HTTP requests
app = FastAPI(
    title=Config.APP_NAME,  # Application name from config
    description="A production-ready REST API for managing book data with PostgreSQL database.",  # API description
    version=Config.APP_VERSION,  # Application version from config
    lifespan=lifespan,  # Lifecycle event handler
    docs_url="/docs",  # URL for Swagger UI documentation
    redoc_url="/redoc",  # URL for ReDoc documentation
    openapi_url="/openapi.json",  # URL for OpenAPI schema JSON
)


# Add CORS middleware
# This allows cross-origin requests from web applications
# In production, you should restrict origins to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Global exception handler
# This catches any unhandled exceptions and returns a proper JSON response
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.

    This catches any exceptions that aren't handled by route handlers
    and returns a proper JSON error response instead of crashing the application.

    Args:
        request: The HTTP request that caused the exception
        exc: The exception that was raised

    Returns:
        JSONResponse with error details
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if Config.DB_ECHO else "An unexpected error occurred",
        },
    )


# Health check endpoint
# This is useful for monitoring and load balancers
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Check if the API is running and healthy",
)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Dictionary with health status
    """
    return {
        "status": "healthy",
        "app_name": Config.APP_NAME,
        "version": Config.APP_VERSION,
    }


# Include routers
# This registers all the route handlers from the books module
app.include_router(
    book_router,
    prefix=Config.API_V1_PREFIX,  # Prefix from config (e.g., "/api/v1")
    tags=["books"],  # Tag for API documentation grouping
)

app.include_router(
    auth_router,
    prefix=Config.API_V1_PREFIX,
    tags=["auth"]
)
