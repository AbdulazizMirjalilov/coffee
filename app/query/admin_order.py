from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Order, OrderItem
from app.models.order import OrderStatus


async def get_all_orders(db: AsyncSession) -> Sequence[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .order_by(desc(Order.created_at))
    )
    return result.scalars().all()


async def update_order_status(
    db: AsyncSession, order_id: UUID, status: OrderStatus
) -> type[Order]:
    order = await db.get(Order, order_id)
    if not order:
        raise ValueError("Order not found")

    order.status = status
    await db.commit()
    await db.refresh(order)
    return order
