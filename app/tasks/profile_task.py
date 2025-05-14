import asyncio
import json
from uuid import UUID

import aiohttp

from app.core.config import settings
from app.services.redis import redis_service
from app.workers.celery import celery

PROFILE_URL = settings.PROFILE_SERVICE_URL


async def profile_request(user_id: UUID):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{PROFILE_URL}/profiles",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"id": str(user_id)}),
            timeout=aiohttp.ClientTimeout(total=5),
        ) as response:
            if response.status >= 400:
                error_text = await response.text()
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"HTTP Error {response.status}: {error_text}",
                )
            return await response.json()


@celery.task(name="profile_task", bind=True, max_retries=3, default_retry_delay=5)
def create_profile(self, user_id: UUID):
    try:
        asyncio.run(profile_request(user_id))
    except (TimeoutError, aiohttp.ClientError):
        if self.request.retries == self.max_retries:
            asyncio.run(redis_service.lpush("failed_profile_tasks", str(user_id)))


@celery.task(name="failed_profile_tasks")
def failed_profile_tasks():
    while True:
        user_id = asyncio.run(redis_service.rpop("failed_profile_tasks"))
        if not user_id:
            break
        create_profile.delay(user_id)
