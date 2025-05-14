from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from app.core.config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

async_engine = create_async_engine(url=DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(async_engine)


async def async_get_db() -> AsyncGenerator[Any, Any]:
    async with async_session() as db:
        yield db
