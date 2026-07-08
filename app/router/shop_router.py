import app.controller.shop_controller as shop_controller
from fastapi import APIRouter, status, Depends, HTTPException
from app.schema.shop_schema import Create, Update, Response, ListResponse
from app.middlewares.authenticate_user import get_current_user

shop_router = APIRouter(prefix="/shop", tags=["Shop"])


@shop_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response)
def create(data: Create, user_id=Depends(get_current_user)):
    shop = shop_controller.create(user_id, data)
    return {"status": 201, "success": True, "message": "shop created successfully", "data": shop}


@shop_router.get("/", status_code=status.HTTP_200_OK, response_model=ListResponse)
def get_all(user_id=Depends(get_current_user)):
    shops = shop_controller.get_all(user_id)
    return {"status": 200, "success": True, "message": "shops fetched successfully", "data": shops}

@shop_router.patch("/{shop_id}", response_model=Response)
def update(shop_id: str, data: Update, user_id=Depends(get_current_user)):
    shop = shop_controller.update(user_id, shop_id, data)
    return {"status": 200, "success": True, "message": "shop updated successfully", "data": shop}


@shop_router.get("/{shop_id}", response_model=Response)
def get(shop_id: str, user_id=Depends(get_current_user)):
    shop = shop_controller.get(user_id, shop_id)
    return {"status": 200, "success": True, "message": "shop fetched successfully", "data": shop}


@shop_router.delete("/{shop_id}", response_model=Response)
def delete(shop_id: str, user_id=Depends(get_current_user)):
    shop_controller.delete(user_id, shop_id)
    return {"status": 200, "success": True, "message": "shop deleted successfully", "data": None}
