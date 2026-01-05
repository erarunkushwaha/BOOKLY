from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import ReviewCreateModel
from fastapi import HTTPException,status
import uuid

class ReviewService:
    @staticmethod
    async def add_review_to_book(
        review_data: ReviewCreateModel,
        user_email: str,
        book_uid: uuid.UUID,
        session: AsyncSession
    ) :

        try:
            book = await BookService.get_book_by_id(book_uid=book_uid,session=session)
            user   = await UserService.get_user_by_email(email=user_email,session=session)
            
            new_review = Reviews(**review_data.model_dump())
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            return new_review
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="oops something went wring..")