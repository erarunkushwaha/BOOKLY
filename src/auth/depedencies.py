from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from typing import Any, List
from .utils import decode_token
from fastapi.security.http import HTTPAuthorizationCredentials
from src.db.redis import token_in_block_list
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import UserService
from typing import List
from src.db.models import User




class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creads = await super().__call__(request)
        token = creads.credentials  # pyright: ignore[reportOptionalMemberAccess]
        token_data = decode_token(token)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"this token is invalid or has been revoked",
                    "resolution":"Please get new token"
                }
            )
            
        if await token_in_block_list(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"this token is invalid or has been revoked",
                    "resolution":"Please get new token"
                }
            )
        
        self.verify_token_data(token_data) # pyright: ignore[reportArgumentType]

        return token_data  # type: ignore

        
    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please overide this method in child classes")
    


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:

        if token_data and token_data["refresh"]:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:

        if token_data and not token_data["refresh"]:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide refresh token"
            )

async def get_current_user(
    token_details:dict = Depends(AccessTokenBearer()),
    session:AsyncSession = Depends(get_session)
    ):
    user_email = token_details["user"]["email"]
    user = await UserService.get_user_by_email(user_email,session=session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user:User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not permitted to access this action")