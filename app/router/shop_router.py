import app.controller.shop_controller as shop_controller
from fastapi import APIRouter, status, Depends, HTTPException
from app.schema import shop_schema
from app.middlewares.authenticate_user import get_current_user
shop_router = APIRouter(prefix="/shop", tags=["Shop"])


@shop_router.post("/", status_code=status.HTTP_201_CREATED, response_model=shop_schema.ShopResponseSchema)
def create_shop(shop: shop_schema.ShopCreateSchema, get_current_user_id=Depends(get_current_user)):
    inserted_shop = shop_controller.create_shop(get_current_user_id, shop)
    print(inserted_shop)
    return inserted_shop


@shop_router.put("/{shop_id}", response_model=shop_schema.ShopResponseSchema)
def update_shop(shop_id: str, shop: shop_schema.ShopUpdateSchema, get_current_user_id=Depends(get_current_user)):
    return shop_controller.update_shop(get_current_user_id, shop_id, shop)


@shop_router.get("/{shop_id}", response_model=shop_schema.ShopResponseSchema)
def get_shop_by_id(shop_id: str, get_current_user_id=Depends(get_current_user)):
    return shop_controller.get_shop_by_id(get_current_user_id, shop_id)


@shop_router.delete("/{shop_id}")
def delete_shop_by_id(shop_id: str, get_current_user_id=Depends(get_current_user)):
    return shop_controller.delete_shop_by_id(get_current_user_id, shop_id)
