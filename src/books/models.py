from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlalchemy.sql import func


class Book(SQLModel, table=True):
    
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )

    title: str
    author: str
    publication: str
    price: float

    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            server_default=func.now()
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            onupdate=func.now()
        )
    )
    
    def __repr__(self):
        return f"<Book {self.title}>"