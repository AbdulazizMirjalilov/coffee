import json
from typing import Any

from redis.asyncio import Redis

from app.core.redis import get_redis


class RedisService:
    def __init__(self, redis_client: Redis | None = None):
        self.redis = redis_client or get_redis()

    async def set(self, key: str, value: Any, expires_in: int | None = None) -> None:
        if isinstance(value, (dict | list)):
            value = json.dumps(value)

        if expires_in:
            await self.redis.setex(key, expires_in, value)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str) -> Any:
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self.redis.exists(key))

    async def setex(self, key: str, expires_in: int, value: Any) -> None:
        if isinstance(value, (dict | list)):
            value = json.dumps(value)
        await self.redis.setex(key, expires_in, value)

    async def lpush(self, key: str, value: Any) -> None:
        await self.redis.lpush(key, value)

    async def rpop(self, key: str) -> Any:
        return await self.redis.rpop(key)


redis_service = RedisService()
