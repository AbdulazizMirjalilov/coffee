from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_order_time: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")  # NOQA
    product: Mapped["Product"] = relationship()  # NOQA
