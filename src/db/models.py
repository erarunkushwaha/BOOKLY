from sqlmodel import SQLModel,Field,Relationship
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column,Index
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func




class User(SQLModel, table=True):
    uid:uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
        index=True,
        description="Unique identifier for the user"
    )
    
    username:str = Field(
        ...,
        max_length=200,
        description="username of user",
        index=True,
        
    )
    
    email:str = Field(
        ...,
        max_length=300,
        description="email of the user",
        unique=True,
        nullable=False
    )
    
    first_name:str
    last_name:str
    role:str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified:bool = Field(default=False)
    password_hash:str = Field(exclude=True)
    
    books:List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':"selectin"})
    
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

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    
"""
SQLModel database models for the Bookly application.

This module defines the database table models using SQLModel, which combines
SQLAlchemy's ORM capabilities with Pydantic's validation.
"""



class Book(SQLModel, table=True):
    
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
    
    user_uid:Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    user:Optional["User"] = Relationship(back_populates="books")

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
    
    
    
class Reviews(SQLModel, table=True):
    
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
    
    rating: int = Field(lt=5)
    review_text:str
    
    user_uid:Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    book_uid:Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    
    user:Optional["User"] = Relationship(back_populates="books")

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
    
 
    
    def __repr__(self) -> str:
      
        return f"<Reviews For Book ########################## {self.uid} by user {self.user_uid}'>"
    

    
    
    