from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.models.user import User
from app.query.admin_order import get_all_orders, update_order_status
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.services.permission import admin_required

router = APIRouter(prefix="/admin/orders", tags=["admin:orders"])


@router.get("/", response_model=list[OrderResponse])
async def list_all_orders(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    _admin: Annotated[User, Depends(admin_required)],
):
    return await get_all_orders(db)


@router.patch("/{order_id}", response_model=OrderResponse)
async def change_order_status(
    order_id: UUID,
    data: OrderStatusUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    _admin: Annotated[User, Depends(admin_required)],
):
    try:
        return await update_order_status(db, order_id, data.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
