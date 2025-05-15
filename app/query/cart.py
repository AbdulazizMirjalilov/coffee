from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import CartItem, Product
from app.schemas.cart import CartItemCreate


async def get_cart_total_by_user(db: AsyncSession, user_id: UUID) -> float:
    result = await db.execute(
        select(func.sum(CartItem.quantity * Product.price))
        .join(Product, CartItem.product_id == Product.id)
        .where(CartItem.user_id == user_id)
    )
    return round(result.scalar() or 0.0, 2)


async def get_cart_items_by_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(
            CartItem, func.sum(CartItem.quantity * Product.price).label("total_price")
        )
        .join(Product, CartItem.product_id == Product.id)
        .options(selectinload(CartItem.product))
        .where(CartItem.user_id == user_id)
    )
    return result.scalars().all()


async def get_cart_item_by_user_and_product(
    db: AsyncSession, user_id: UUID, product_id: UUID
):
    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == user_id, CartItem.product_id == product_id
        )
    )
    return result.scalar_one_or_none()


async def add_or_update_cart_item(
    db: AsyncSession, user_id: UUID, data: CartItemCreate
):
    item = await get_cart_item_by_user_and_product(db, user_id, data.product_id)
    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            user_id=user_id, product_id=data.product_id, quantity=data.quantity
        )
        db.add(item)

    await db.commit()
    await db.refresh(item)
    return item


async def update_cart_item_quantity(db: AsyncSession, item: CartItem, quantity: int):
    item.quantity = quantity
    await db.commit()
    await db.refresh(item)
    return item


async def delete_cart_item(db: AsyncSession, item: CartItem):
    await db.delete(item)
    await db.commit()
