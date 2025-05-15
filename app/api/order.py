from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.models.user import User
from app.query.order import create_order_from_cart, get_user_orders
from app.schemas.order import OrderResponse
from app.services.user import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout", response_model=OrderResponse)
async def checkout(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        order = await create_order_from_cart(db, current_user.id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await get_user_orders(db, current_user.id)
