"""
SQLModel database models for the Bookly application.

This module defines the database table models using SQLModel, which combines
SQLAlchemy's ORM capabilities with Pydantic's validation.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, Index
from sqlalchemy.sql import func


class Book(SQLModel, table=True):
    """
    Book database model.
    
    This class represents the 'book' table in PostgreSQL. SQLModel automatically
    creates the table based on this model definition when the database is initialized.
    
    Attributes:
        uid: Unique identifier (UUID) for the book, primary key
        title: Title of the book
        author: Author of the book
        publication: Publication house name
        price: Price of the book
        created_at: Timestamp when the book was created (auto-generated)
        updated_at: Timestamp when the book was last updated (auto-updated)
    """
    
    # Primary key: UUID field
    # Using UUID instead of integer ID provides better security and scalability
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,  # Automatically generate UUID if not provided
        sa_column=Column(
            pg.UUID(as_uuid=True),  # Use PostgreSQL UUID type
            primary_key=True,  # Set as primary key
            nullable=False,  # Cannot be null
            index=True,  # Create index for faster lookups
        ),
        description="Unique identifier for the book"
    )

    # Book information fields
    title: str = Field(
        ...,
        max_length=200,  # Maximum length constraint
        description="Title of the book",
        index=True,  # Create index for faster searches by title
    )
    
    author: str = Field(
        ...,
        max_length=100,
        description="Author of the book",
        index=True,  # Create index for faster searches by author
    )
    
    publication: str = Field(
        ...,
        max_length=100,
        description="Publication house name"
    )
    
    price: float = Field(
        ...,
        gt=0,  # Must be greater than 0
        description="Price of the book in currency units"
    )

    # Timestamp fields
    # These are automatically managed by the database
    created_at: datetime = Field(
        default=None,  # Will be set by database
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),  # Use PostgreSQL timestamp with timezone
            server_default=func.now(),  # Default to current timestamp on insert
            nullable=False,
        ),
        description="Timestamp when the book was created"
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            onupdate=func.now(),  # Automatically update to current timestamp on update
            nullable=True,  # Can be null initially
        ),
        description="Timestamp when the book was last updated"
    )
    
    # Create composite index for common query patterns
    # This improves performance when filtering by author and title together
    __table_args__ = (
        Index('idx_book_author_title', 'author', 'title'),
    )
    
    def __repr__(self) -> str:
        """
        String representation of the Book instance.
        
        Returns:
            A string representation showing the book title
        """
        return f"<Book(uid={self.uid}, title='{self.title}')>"
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        
        Returns:
            A formatted string with book details
        """
        return f"{self.title} by {self.author} - ${self.price}"