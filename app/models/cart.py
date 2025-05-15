import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.base_model import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="cart_items")  # NOQA
    product: Mapped["Product"] = relationship()  # NOQA

    quantity: Mapped[int] = mapped_column(default=1)
