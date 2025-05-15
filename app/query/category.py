from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def create_category_query(db: AsyncSession, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_all_categories_query(db: AsyncSession) -> Sequence[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category_by_id_query(
    db: AsyncSession, category_id: UUID
) -> Category | None:
    result = await db.execute(select(Category).where(category_id == Category.id))
    return result.scalar_one_or_none()


async def update_category_query(
    db: AsyncSession, category: Category, data: CategoryUpdate
) -> Category:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category_query(db: AsyncSession, category: Category):
    await db.delete(category)
    await db.commit()
