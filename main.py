"""
Application entry point.

This is the main entry point for running the FastAPI application.
It can be run directly with Python or using uvicorn from the command line.

Usage:
    python main.py
    or
    uvicorn main:app --reload
"""

import uvicorn
from src import app
from src.config import Config

if __name__ == "__main__":
    """
    Run the FastAPI application using uvicorn.
    
    This is the development server. For production, use a proper ASGI server
    like uvicorn with multiple workers behind a reverse proxy (nginx).
    
    Configuration:
        - host: Listen on all interfaces (0.0.0.0)
        - port: Port number (default 8000)
        - reload: Auto-reload on code changes (development only)
        - log_level: Logging level
    """
    uvicorn.run(
        "src:app",  # Application instance to run
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,  # Port number
        reload=True,  # Auto-reload on code changes (disable in production)
        log_level="info"  # Logging level
    )

