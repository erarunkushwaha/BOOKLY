from fastapi import APIRouter, Depends, status
from .schema import UserCreateModel, UserResponse
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException


auth_router = APIRouter(
    prefix="/auth",
)
user_service = UserService()


@auth_router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exist = await user_service.user_exist(email, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user already exist with this email",
        )

    new_user = await UserService.create_user(user_data, session)

    return new_user
