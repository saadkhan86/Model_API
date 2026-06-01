import app.controller.shop_controller as shop_controller
from fastapi import APIRouter, status, Depends, HTTPException
from app.schema.shop_schema import ShopCreateSchema, ShopResponseSchema, ShopUpdateSchema, ShopResponseModel
from app.middlewares.authenticate_user import get_current_user

shop_router = APIRouter(prefix="/shop", tags=["Shop"])


@shop_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShopResponseModel)
def create_shop(data: ShopCreateSchema, user_id=Depends(get_current_user)):
    shop = shop_controller.create_shop(user_id, data)
    return {"status": 201, "success": True, "message": "shop created successfully", "data": shop}


@shop_router.put("/{shop_id}", response_model=ShopResponseModel)
def update_shop(shop_id: str, data: ShopUpdateSchema, user_id=Depends(get_current_user)):
    shop = shop_controller.update_shop(user_id, shop_id, data)
    return {"status": 200, "success": True, "message": "shop updated successfully", "data": shop}


@shop_router.get("/{shop_id}", response_model=ShopResponseModel)
def get_shop(shop_id: str, user_id=Depends(get_current_user)):
    shop = shop_controller.get_shop(user_id, shop_id)
    return {"status": 200, "success": True, "message": "shop fetched successfully", "data": shop}


@shop_router.delete("/{shop_id}", response_model=ShopResponseModel)
def delete_shop(shop_id: str, user_id=Depends(get_current_user)):
    shop_controller.delete_shop(user_id, shop_id)
    return {"status": 200, "success": True, "message": "shop deleted successfully", "data": None}
