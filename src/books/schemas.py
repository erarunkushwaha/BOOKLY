"""
Pydantic schemas for book data validation and serialization.

This module defines the request/response models for the book API endpoints.
Pydantic automatically validates incoming data and serializes outgoing data.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class BookBase(BaseModel):
    """
    Base schema with common book fields.
    
    This is used as a base class for other schemas to avoid code duplication.
    """
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the book",
        examples=["The Alchemist"]
    )
    
    author: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Author of the book",
        examples=["Paulo Coelho"]
    )
    
    publication: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Publication house name",
        examples=["HarperCollins"]
    )
    
    price: float = Field(
        ...,
        gt=0,
        description="Price of the book in currency units",
        examples=[399.99]
    )
    
    @field_validator("title", "author", "publication")
    @classmethod
    def validate_string_fields(cls, v: str) -> str:
        """
        Validate and sanitize string fields.
        
        Args:
            v: The string value to validate
            
        Returns:
            Stripped string value
            
        Raises:
            ValueError: If the string is empty after stripping
        """
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class BookCreate(BookBase):
    """
    Schema for creating a new book.
    
    This schema is used when receiving POST requests to create a book.
    It inherits all fields from BookBase.
    """
    pass


class BookUpdate(BaseModel):
    """
    Schema for updating an existing book.
    
    All fields are optional, allowing partial updates.
    Only provided fields will be updated.
    """
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Title of the book",
        examples=["The Alchemist"]
    )
    
    author: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Author of the book",
        examples=["Paulo Coelho"]
    )
    
    publication: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Publication house name",
        examples=["HarperCollins"]
    )
    
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Price of the book in currency units",
        examples=[399.99]
    )
    
    @field_validator("title", "author", "publication", mode="before")
    @classmethod
    def validate_optional_string_fields(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate optional string fields.
        
        Args:
            v: The optional string value to validate
            
        Returns:
            Stripped string value or None
        """
        if v is not None:
            if not v.strip():
                raise ValueError("Field cannot be empty or whitespace only")
            return v.strip()
        return v


class BookResponse(BookBase):
    """
    Schema for book response data.
    
    This schema is used when returning book data in API responses.
    It includes all base fields plus metadata fields (uid, timestamps).
    """
    
    uid: uuid.UUID = Field(
        ...,
        description="Unique identifier for the book",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp when the book was created",
        examples=["2024-01-15T10:30:00Z"]
    )
    
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the book was last updated",
        examples=["2024-01-15T10:30:00Z"]
    )
    
    # Pydantic v2 configuration
    model_config = ConfigDict(
        # Use enum values instead of enum names
        use_enum_values=True,
        # Validate assignment (check types when assigning to model instances)
        validate_assignment=True,
        # Serialize datetime and UUID properly
        json_encoders={
            datetime: lambda v: v.isoformat(),  # Convert datetime to ISO format
            uuid.UUID: lambda v: str(v),  # Convert UUID to string
        },
        # Example data for API documentation
        json_schema_extra={
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "publication": "HarperCollins",
                "price": 399.99,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
    )