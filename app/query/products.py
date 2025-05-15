from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product_query(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_all_products_query(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> Sequence[Product]:
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


async def get_product_by_id_query(db: AsyncSession, product_id: UUID) -> Product | None:
    result = await db.execute(select(Product).where(product_id == Product.id))
    return result.scalar_one_or_none()


async def update_product_query(
    db: AsyncSession, product: Product, data: ProductUpdate
) -> Product:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product_query(db: AsyncSession, product: Product):
    await db.delete(product)
    await db.commit()
