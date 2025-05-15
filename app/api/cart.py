from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.models.user import User
from app.query.cart import (
    add_or_update_cart_item,
    delete_cart_item,
    get_cart_item_by_user_and_product,
    get_cart_items_by_user,
    get_cart_total_by_user,
    update_cart_item_quantity,
)
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
)
from app.services.user import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
async def get_my_cart(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    items = await get_cart_items_by_user(db, current_user.id)
    total = await get_cart_total_by_user(db, current_user.id)
    return CartResponse(items=items, total=total)


@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    data: CartItemCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await add_or_update_cart_item(db, current_user.id, data)


@router.patch("/{product_id}", response_model=CartItemResponse)
async def update_cart_quantity(
    product_id: UUID,
    data: CartItemUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    item = await get_cart_item_by_user_and_product(db, current_user.id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    return await update_cart_item_quantity(db, item, data.quantity)


@router.delete("/{product_id}")
async def remove_from_cart(
    product_id: UUID,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    item = await get_cart_item_by_user_and_product(db, current_user.id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    await delete_cart_item(db, item)
    return {"message": "Removed from cart"}
