from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.query.products import (
    create_product_query,
    delete_product_query,
    get_all_products_query,
    get_product_by_id_query,
    update_product_query,
)
from app.schemas.paggination import Pagination
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.permission import admin_required

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    return await create_product_query(db, data)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    pagination: Annotated[Pagination, Depends()],
    db: AsyncSession = Depends(async_get_db),
):
    return await get_all_products_query(
        db, skip=pagination.skip, limit=pagination.limit
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, db: AsyncSession = Depends(async_get_db)):
    product = await get_product_by_id_query(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    product = await get_product_by_id_query(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return await update_product_query(db, product, data)


@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    product = await get_product_by_id_query(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await delete_product_query(db, product)
    return {"message": "Product deleted successfully"}
