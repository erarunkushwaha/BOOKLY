"""
Configuration module for the Bookly application.

This module handles all application settings and environment variables
using Pydantic Settings for type-safe configuration management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class uses Pydantic Settings to automatically load configuration
    from environment variables or a .env file. All settings are type-validated
    and can have default values.
    """
    
    # Database configuration
    # Format: postgresql+asyncpg://user:password@host:port/database
    DATABASE_URL: str = Field(
        default="",
        description="PostgreSQL database connection URL with asyncpg driver"
    )
    
    JWT_SECRET_KEY: str = Field(
    default="",
    description="JWT secret key"
    )
    
    JWT_ALGORITHM: str = Field(
    default="",
    description="JWT ALGORITHM"
    )
    
    ACCESS_TOKEN_EXPIRY: int = Field(
    default=3600,
    description="JWT EXPIRY TIME"
    )
    
    REFRESH_TOKEN_EXPIRY: int = Field(
        default=2,
        description=""
    )
    REDIS_HOST: str = Field(
        default="",
        description=""
    )
    
    REDIS_PORT: int = Field(
        default=6379,
        description=""
    )
    

    
    
    # Application settings
    APP_NAME: str = Field(
        default="Bookly API",
        description="Application name"
    )
    
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version"
    )
    
    # Database connection pool settings
    DB_POOL_SIZE: int = Field(
        default=5,
        description="Number of connections to maintain in the connection pool"
    )
    
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        description="Maximum number of connections to allow beyond pool_size"
    )
    
    DB_ECHO: bool = Field(
        default=False,
        description="Enable SQL query logging (set to True for debugging)"
    )
    
    # API settings
    API_V1_PREFIX: str = Field(
        default="/api/v1",
        description="API version 1 prefix for all routes"
    )
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """
        Validate that DATABASE_URL is provided and properly formatted.
        
        Args:
            v: The database URL string to validate
            
        Returns:
            The validated database URL
            
        Raises:
            ValueError: If DATABASE_URL is empty or invalid
        """
        if not v:
            raise ValueError(
                "DATABASE_URL must be set. "
                "Format: postgresql+asyncpg://user:password@host:port/database"
            )
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError(
                "DATABASE_URL must use postgresql+asyncpg:// protocol"
            )
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",  # Load from .env file if present
        env_file_encoding="utf-8",  # Use UTF-8 encoding for .env file
        case_sensitive=True,  # Environment variable names are case-sensitive
        extra="ignore",  # Ignore extra fields not defined in the model
    )


# Create a singleton instance of Settings
# This will be imported throughout the application
Config = Settings()