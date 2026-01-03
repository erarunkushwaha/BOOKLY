"""
API routes for book operations.

This module defines all the HTTP endpoints for the book API.
It handles request/response conversion and delegates business logic to the service layer.
"""

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
import logging

from src.db.main import get_session
from src.books.schemas import BookCreate, BookUpdate, BookResponse
from src.books.service import BookService, BookNotFoundError
from src.auth.depedencies import AccessTokenBearer


# Configure logging
logger = logging.getLogger(__name__)


access_token_bearer = AccessTokenBearer()
# Create router with prefix and tags for better organization
# The prefix will be combined with the app's prefix in main.py
book_router = APIRouter(
    prefix="/books",
    tags=["books"],  # Groups endpoints in API documentation
    responses={
        404: {"description": "Book not found"},
        500: {"description": "Internal server error"}
    }
)


@book_router.get(
    "/",
    response_model=List[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all books",
    description="Retrieve a list of all books in the database, ordered by creation date (newest first).",
    response_description="List of all books"
)
async def get_all_books(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip (for pagination)",
        example=0
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of records to return (for pagination)",
        example=100
    ),
    session: AsyncSession = Depends(get_session),
    user_details = Depends(access_token_bearer)
) -> List[BookResponse]:
    """
    Retrieve all books from the database.
    
    This endpoint returns a paginated list of all books. The books are ordered
    by creation date in descending order (newest first).
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        session: Database session (injected by FastAPI dependency)
        
    Returns:
        List of BookResponse objects
        
    Raises:
        HTTPException: If there's an error retrieving books from the database
    """
    
    print("user details- ########################",user_details)
    try:
        # Call the service layer to get all books
        books = await BookService.get_all_books(session, skip=skip, limit=limit)
        
        # Convert SQLModel objects to Pydantic response models
        # Use from_attributes=True to convert ORM objects to Pydantic models
        return [BookResponse.model_validate(book, from_attributes=True) for book in books]
        
    except Exception as e:
        logger.error(f"Error in get_all_books endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )


@book_router.get(
    "/{book_uid}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Get book by ID",
    description="Retrieve a single book by its UUID.",
    response_description="Book details"
)
async def get_book(
    book_uid: uuid.UUID,  # Path parameter (from URL path)
    session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """
    Retrieve a single book by its UUID.
    
    Args:
        book_uid: UUID of the book to retrieve
        session: Database session (injected by FastAPI dependency)
        
    Returns:
        BookResponse object with book details
        
    Raises:
        HTTPException: 404 if book not found, 500 if database error occurs
    """
    try:
        # Call the service layer to get the book
        book = await BookService.get_book_by_id(book_uid, session)
        
        # Check if book exists
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with uid {book_uid} not found"
            )
        
        # Convert SQLModel object to Pydantic response model
        # Use from_attributes=True to convert ORM objects to Pydantic models
        return BookResponse.model_validate(book, from_attributes=True)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in get_book endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve book"
        )


@book_router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Create a new book in the database. All fields are required.",
    response_description="The newly created book"
)
async def create_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """
    Create a new book in the database.
    
    This endpoint accepts book data, validates it, and creates a new book record.
    The UUID and timestamps are automatically generated.
    
    Args:
        book: BookCreate schema with book information (title, author, publication, price)
        session: Database session (injected by FastAPI dependency)
        
    Returns:
        BookResponse object with the newly created book details
        
    Raises:
        HTTPException: 400 if validation fails, 500 if database error occurs
    """
    try:
        # Call the service layer to create the book
        new_book = await BookService.create_book(book, session)
        
        # Convert SQLModel object to Pydantic response model
        # Use from_attributes=True to convert ORM objects to Pydantic models
        return BookResponse.model_validate(new_book, from_attributes=True)
        
    except Exception as e:
        logger.error(f"Error in create_book endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}"
        )


@book_router.put(
    "/{book_uid}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a book",
    description="Update an existing book. All fields are optional - only provided fields will be updated.",
    response_description="The updated book"
)
async def update_book(
    book_uid: uuid.UUID,
    book_update: BookUpdate,
    session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """
    Update an existing book in the database.
    
    This endpoint performs a partial update - only the fields provided in the
    request body will be updated. Fields not provided will remain unchanged.
    
    Args:
        book_uid: UUID of the book to update
        book_update: BookUpdate schema with fields to update (all optional)
        session: Database session (injected by FastAPI dependency)
        
    Returns:
        BookResponse object with the updated book details
        
    Raises:
        HTTPException: 404 if book not found, 400 if validation fails, 500 if database error occurs
    """
    try:
        # Call the service layer to update the book
        updated_book = await BookService.update_book(book_uid, book_update, session)
        
        # Convert SQLModel object to Pydantic response model
        # Use from_attributes=True to convert ORM objects to Pydantic models
        return BookResponse.model_validate(updated_book, from_attributes=True)
        
    except BookNotFoundError as e:
        # Convert service layer exception to HTTP exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in update_book endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Delete a book from the database by its UUID.",
    response_description="No content (book deleted successfully)"
)
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a book from the database.
    
    This endpoint permanently deletes a book from the database.
    The operation cannot be undone.
    
    Args:
        book_uid: UUID of the book to delete
        session: Database session (injected by FastAPI dependency)
        
    Returns:
        None (204 No Content status)
        
    Raises:
        HTTPException: 404 if book not found, 500 if database error occurs
    """
    try:
        # Call the service layer to delete the book
        await BookService.delete_book(book_uid, session)
        
        # Return None (FastAPI will send 204 No Content)
        return None
        
    except BookNotFoundError as e:
        # Convert service layer exception to HTTP exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in delete_book endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}"
        )
