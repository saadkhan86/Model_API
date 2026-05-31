from app.router.user_router import user_router
from app.router.shop_router import shop_router
from fastapi import APIRouter
router = APIRouter(prefix="/api/v1", tags=["all"])


router.include_router(user_router)
router.include_router(shop_router)
