from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/signup")

async def signup():
    pass