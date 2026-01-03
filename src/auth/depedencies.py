
from fastapi import Request,HTTPException,status
from fastapi.security import HTTPBearer
from typing import List
from .utils import decode_token

from fastapi.security.http import HTTPAuthorizationCredentials

class AccessTokenBearer(HTTPBearer):
    
    def __init(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creads =  await super().__call__(request)
        token = creads.credentials  # pyright: ignore[reportOptionalMemberAccess]
        token_data = decode_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        
        if token_data['refresh']:  # type: ignore
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provide access token")
        
        return token_data # type: ignore
    
    def token_valid(self, token:str) -> bool:
        token_data = decode_token(token)
        
        if token_data:
            return True
        else:
            return False