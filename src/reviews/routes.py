from fastapi import APIRouter, Depends
from src.db.models import User
from src.db.main import get_session 
from src.auth.depedencies import get_current_user
from .schemas import ReviewCreateModel
from sqlalchemy.ext.asyncio import AsyncSession
from .service import ReviewService
import uuid


review_router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@review_router.get("/")
async def get_reviews():
    return {"message": "Hello, World!"}


@review_router.post("/book/{book_uid}")
async def add_review_to_book( book_uid:uuid.UUID,  review_data:ReviewCreateModel, current_user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
   await ReviewService.add_review_to_book(user_email=current_user.email, review_data=review_data, book_uid=book_uid, session=session)