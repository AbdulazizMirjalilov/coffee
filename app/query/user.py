from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.security import get_password_hash


async def create_user_query(db: AsyncSession, data: dict) -> UUID:
    hashed_password = get_password_hash(data["password"])
    data["password"] = hashed_password
    user = User(**data, is_verified=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user.id


async def get_user_by_email_query(db: AsyncSession, email: str):
    data = await db.execute(select(User).where(User.email == email))
    return data.scalar()
