"""
Service layer for book operations.

This module contains the business logic for book CRUD operations.
It acts as an abstraction layer between the API routes and the database,
making the code more maintainable and testable.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from typing import List, Optional
import uuid
import logging

from src.books.schemas import BookCreate, BookUpdate
from src.books.models import Book

# Configure logging
logger = logging.getLogger(__name__)


class BookNotFoundError(Exception):
    """
    Custom exception raised when a book is not found.
    
    This provides a clear way to handle book not found scenarios
    and allows the route layer to convert it to appropriate HTTP responses.
    """
    pass


class BookService:
    """
    Service class for book-related database operations.
    
    This class encapsulates all database operations related to books,
    providing a clean interface for the route handlers.
    """
    
    @staticmethod
    async def get_all_books(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Retrieve all books from the database.
        
        Args:
            session: Database session for executing queries
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return (for pagination)
            
        Returns:
            List of Book objects, ordered by creation date (newest first)
            
        Note:
            In production, you should implement proper pagination
            to avoid loading too many records at once.
        """
        try:
            # Create a SELECT query
            # order_by(desc(...)) sorts by created_at in descending order (newest first)
            statement = select(Book).order_by(desc(Book.created_at))
            
            # Apply pagination
            statement = statement.offset(skip).limit(limit)
            
            # Execute the query using SQLAlchemy's async execute method
            # scalars() returns scalar results (single column/object results)
            result = await session.execute(statement)
            
            # Get all results as a list
            books = result.scalars().all()
            
            logger.info(f"Retrieved {len(books)} books from database")
            return books
            
        except Exception as e:
            logger.error(f"Error retrieving books: {e}")
            raise
    
    @staticmethod
    async def get_book_by_id(
        book_uid: uuid.UUID,
        session: AsyncSession
    ) -> Optional[Book]:
        """
        Retrieve a single book by its UUID.
        
        Args:
            book_uid: UUID of the book to retrieve
            session: Database session for executing queries
            
        Returns:
            Book object if found, None otherwise
        """
        try:
            # Create a SELECT query with WHERE clause
            statement = select(Book).where(Book.uid == book_uid)
            
            # Execute the query using SQLAlchemy's async execute method
            # scalars() returns scalar results (single column/object results)
            result = await session.execute(statement)
            
            # Get the first result (should be unique since uid is primary key)
            book = result.scalar_one_or_none()
            
            if book:
                logger.info(f"Retrieved book with uid: {book_uid}")
            else:
                logger.warning(f"Book with uid {book_uid} not found")
            
            return book
            
        except Exception as e:
            logger.error(f"Error retrieving book {book_uid}: {e}")
            raise
    
    @staticmethod
    async def create_book(
        book_data: BookCreate,
        session: AsyncSession
    ) -> Book:
        """
        Create a new book in the database.
        
        Args:
            book_data: BookCreate schema with book information
            session: Database session for executing queries
            
        Returns:
            The newly created Book object
            
        Raises:
            Exception: If database operation fails
        """
        try:
            # Convert Pydantic model to dictionary
            book_data_dict = book_data.model_dump()
            
            # Create a new Book instance
            # SQLModel will automatically generate the UUID if not provided
            new_book = Book(**book_data_dict)
            
            # Add the book to the session
            session.add(new_book)
            
            # Flush to get the generated UUID and timestamps
            await session.flush()
            
            # Refresh to load any database-generated values
            await session.refresh(new_book)
            
            # Commit the transaction
            await session.commit()
            
            logger.info(f"Created new book: {new_book.title} (uid: {new_book.uid})")
            return new_book
            
        except Exception as e:
            logger.error(f"Error creating book: {e}")
            # Rollback the transaction on error
            await session.rollback()
            raise
    
    @staticmethod
    async def update_book(
        book_uid: uuid.UUID,
        book_data: BookUpdate,
        session: AsyncSession
    ) -> Book:
        """
        Update an existing book in the database.
        
        This method performs a partial update - only provided fields are updated.
        Fields that are not provided in book_data remain unchanged.
        
        Args:
            book_uid: UUID of the book to update
            book_data: BookUpdate schema with fields to update (all optional)
            session: Database session for executing queries
            
        Returns:
            The updated Book object
            
        Raises:
            BookNotFoundError: If the book with the given UUID doesn't exist
            Exception: If database operation fails
        """
        try:
            # 1. Fetch the book from the database
            book_to_update = await BookService.get_book_by_id(book_uid, session)
            
            # 2. Check if book exists
            if not book_to_update:
                raise BookNotFoundError(f"Book with uid {book_uid} not found")
            
            # 3. Get only the fields that were provided (exclude_unset=True)
            # This allows partial updates - only update fields that were sent
            update_data = book_data.model_dump(exclude_unset=True)
            
            # 4. Check if there's anything to update
            if not update_data:
                logger.info(f"No fields to update for book {book_uid}")
                return book_to_update
            
            # 5. Update fields dynamically
            # This allows us to update only the fields that were provided
            for key, value in update_data.items():
                setattr(book_to_update, key, value)
            
            # 6. Add the updated book to the session
            session.add(book_to_update)
            
            # 7. Flush to apply changes (but don't commit yet)
            await session.flush()
            
            # 8. Refresh to get updated timestamps from database
            await session.refresh(book_to_update)
            
            # 9. Commit the transaction
            await session.commit()
            
            logger.info(f"Updated book with uid: {book_uid}")
            return book_to_update
            
        except BookNotFoundError:
            # Re-raise BookNotFoundError as-is
            raise
        except Exception as e:
            logger.error(f"Error updating book {book_uid}: {e}")
            # Rollback the transaction on error
            await session.rollback()
            raise
    
    @staticmethod
    async def delete_book(
        book_uid: uuid.UUID,
        session: AsyncSession
    ) -> None:
        """
        Delete a book from the database.
        
        Args:
            book_uid: UUID of the book to delete
            session: Database session for executing queries
            
        Raises:
            BookNotFoundError: If the book with the given UUID doesn't exist
            Exception: If database operation fails
        """
        try:
            # 1. Fetch the book from the database
            book_to_delete = await BookService.get_book_by_id(book_uid, session)
            
            # 2. Check if book exists
            if not book_to_delete:
                raise BookNotFoundError(f"Book with uid {book_uid} not found")
            
            # 3. Delete the book
            # delete() is synchronous - it marks the object for deletion in the session
            session.delete(book_to_delete)
            
            # 4. Commit the transaction
            await session.commit()
            
            logger.info(f"Deleted book with uid: {book_uid}")
            
        except BookNotFoundError:
            # Re-raise BookNotFoundError as-is
            raise
        except Exception as e:
            logger.error(f"Error deleting book {book_uid}: {e}")
            # Rollback the transaction on error
            await session.rollback()
            raise