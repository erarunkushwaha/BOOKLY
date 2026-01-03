from fastapi import APIRouter, Depends, status
from .schema import UserCreateModel, UserResponse,UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import generate_access_token, decode_token,verify_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from src.config import Config
from .depedencies import RefreshTokenBearer

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


@auth_router.post("/login", status_code=status.HTTP_200_OK)

async def login(user_data:UserLoginModel, session:AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    
    user =  await UserService.get_user_by_email(email,session)
    
    if user is not None:
        password_valid = verify_password(password,user.password_hash)
        
        if password_valid:
            access_token = generate_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid )
                }
            )
            
            refresh_token = generate_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid )
                },
                refresh=True,
                expiry=timedelta(days=Config.REFRESH_TOKEN_EXPIRY)
                
            )
    
            return JSONResponse(
               content={
                "message":"Login successful",
                "access_token":access_token,
                "refresh_token":refresh_token,
                "user":{
                    "email":user.email,
                    "uid": str(user.uid),
                }
               }
                
            )
            
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid email or password"
    )
    

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    # Token expiry is already validated by decode_token in RefreshTokenBearer
    # If we reach here, the token is valid
    expiry_timestamp = token_details.get('exp')
    
    # Double-check expiry (though it's already validated by JWT decode)
    if expiry_timestamp and datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = generate_access_token(
            user_data=token_details['user']
        )
    
        return JSONResponse(content={
            "access_token": new_access_token
        })
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token"
    )