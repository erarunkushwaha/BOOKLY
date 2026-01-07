from fastapi import Request, HTTPException, status, Depends
from typing import Any,Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BooklyException(Exception):
    """this is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """user has provided an invalid or expired token"""
    pass


class RevokedToken(BooklyException):
    """user has provided an invalid or expired token"""

    pass


def create_exception_handler(status_code:int, initial_details:Any)-> Callable[[Request,Exception],JSONResponse]:
    
    async def exception_handler(request:Request, exc:BooklyException):
        return JSONResponse(
            content=initial_details,
            status_code=status_code
            
        )
    return exception_handler
