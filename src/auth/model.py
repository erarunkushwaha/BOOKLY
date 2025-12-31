from sqlmodel import SQLModel,Field
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column
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
    is_veriied:bool = Field(default=False)
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