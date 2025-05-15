from uuid import UUID

from pydantic import BaseModel

from app.models.order import OrderStatus
from app.schemas.product import ProductResponse


class OrderItemResponse(BaseModel):
    product: ProductResponse
    quantity: int
    price_at_order_time: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: UUID
    total_price: float
    status: str
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
