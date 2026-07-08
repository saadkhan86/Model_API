from app.router.user_router import user_router
from app.router.shop_router import shop_router
from app.router.camera_router import camera_router
from app.router.connection_router import connection_router
from fastapi import APIRouter
router = APIRouter(prefix="/api/v1")


router.include_router(user_router)
router.include_router(shop_router)
router.include_router(connection_router)
router.include_router(camera_router)
