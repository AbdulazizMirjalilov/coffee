import uuid

from app.core.config import settings
from app.schemas.auth import AuthToken
from app.services.security import generate_token

ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE_DAYS
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def auth_token_generate(user_id: uuid.UUID) -> AuthToken:
    access_token = await generate_token(user_id, ACCESS_TOKEN_EXPIRE, "access_token")
    refresh_token = await generate_token(user_id, REFRESH_TOKEN_EXPIRE, "refresh_token")

    return AuthToken(access_token=access_token, refresh_token=refresh_token)


async def auth_token_refresh(user_id: uuid.UUID) -> str:
    return await generate_token(user_id, ACCESS_TOKEN_EXPIRE, "access_token")
