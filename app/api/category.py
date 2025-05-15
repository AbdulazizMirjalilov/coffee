from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.query.category import (
    create_category_query,
    delete_category_query,
    get_all_categories_query,
    get_category_by_id_query,
    update_category_query,
)
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.permission import admin_required

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    return await create_category_query(db, data)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(async_get_db)):
    return await get_all_categories_query(db)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID, db: AsyncSession = Depends(async_get_db)):
    category = await get_category_by_id_query(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    category = await get_category_by_id_query(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return await update_category_query(db, category, data)


@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(admin_required),
):
    category = await get_category_by_id_query(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await delete_category_query(db, category)
    return {"message": "Category deleted successfully"}
