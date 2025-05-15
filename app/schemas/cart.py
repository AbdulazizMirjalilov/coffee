from uuid import UUID

from pydantic import BaseModel

from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: UUID
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: UUID
    product: ProductResponse
    total_price: float
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float
