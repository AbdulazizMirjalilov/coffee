import redis.asyncio as aioredis

from app.core.config import settings

REDIS_CACHE_HOST = settings.REDIS_CACHE_HOST
REDIS_CACHE_PORT = settings.REDIS_CACHE_PORT


def get_redis() -> aioredis.Redis:
    return aioredis.Redis(
        host=REDIS_CACHE_HOST,
        port=REDIS_CACHE_PORT,
        decode_responses=True,
    )
