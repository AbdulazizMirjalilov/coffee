from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import CartItem, Order, OrderItem


async def create_order_from_cart(db: AsyncSession, user_id: UUID) -> Order:
    stmt = (
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.user_id == user_id)
    )
    cart_items = (await db.execute(stmt)).scalars().all()

    if not cart_items:
        raise ValueError("Cart is empty")

    total = 0.0

    order = Order(user_id=user_id, total_price=0.0)
    db.add(order)
    await db.flush()

    for item in cart_items:
        item_total = item.quantity * item.product.price
        total += item_total
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price_at_order_time=item.product.price,
        )
        db.add(order_item)

    order.total_price = round(total, 2)

    for item in cart_items:
        await db.delete(item)

    await db.commit()
    await db.refresh(order)
    return order


async def get_user_orders(db: AsyncSession, user_id: UUID) -> Sequence[Order]:
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()
