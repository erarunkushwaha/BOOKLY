from src.config import Config
from redis.asyncio import Redis

JTI_EXPIRY = 3600

token_blocklist = Redis.from_url(
        "redis://localhost:6379",
        decode_responses=True
    )


async def add_jti_to_block_list(jti:str)-> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    

async def token_in_block_list(jti:str)-> None:
    await token_blocklist.get(name=jti)