import secrets
import string
import uuid
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
WEB_URL = settings.WEB_URL
EMAIL_EXPIRE_SECONDS = settings.EMAIL_EXPIRE_HOURS * 3600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(hashed_password, plain_password)


async def generate_verification_code(length: int = 16) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


async def generate_verification_url(verification_code: str) -> str:
    return f"{WEB_URL}/verify-email?verification_code={verification_code}"


async def generate_token(user_id: uuid.UUID, exp: int, token_type: str) -> str:
    expire = datetime.now() + timedelta(minutes=exp)
    payload = {
        "exp": expire,
        "id": str(user_id),
        "type": token_type,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
