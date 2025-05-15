from fastapi import APIRouter

from .admin_order import router as admin_order_router
from .auth import router as auth_router
from .cart import router as cart_router
from .category import router as category_router
from .order import router as order_router
from .product import router as product_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(cart_router)
router.include_router(order_router)
router.include_router(admin_order_router)
