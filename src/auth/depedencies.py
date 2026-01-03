from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List
from .utils import decode_token
from fastapi.security.http import HTTPAuthorizationCredentials
from src.db.redis import token_in_block_list



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
