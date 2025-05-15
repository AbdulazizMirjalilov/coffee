import uuid
from enum import Enum as BaseEnum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.base_model import BaseModel


class OrderStatus(str, BaseEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    SHIPPED = "shipped"


class Order(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    total_price: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="orders")  # NOQA
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")  # NOQA
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
