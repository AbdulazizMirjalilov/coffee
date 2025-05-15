from uuid import UUID

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: float
    category_id: UUID


class ProductUpdate(BaseModel):
    name: str | None
    description: str | None
    price: float | None
    category_id: UUID | None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: float
    category_id: UUID

    class Config:
        from_attributes = True
