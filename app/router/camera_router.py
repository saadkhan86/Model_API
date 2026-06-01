from fastapi import APIRouter, status, Depends
from app.schema.camera_schema import CameraResponseModel, CameraCreateSchema, CameraUpdateSchema
from app.middlewares.authenticate_user import get_current_user
import app.controller.camera_controller as camera_controller
camera_router = APIRouter(prefix="/camera", tags=["Camera"])


@camera_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CameraResponseModel)
def create(data: CameraCreateSchema, user_id=Depends(get_current_user)):
    camera = camera_controller.create(data, user_id)
    return {"status": 201, "success": True, "message": "camera created successfully", "data": camera}


@camera_router.put("/{camera_id}", response_model=CameraResponseModel)
def update(camera_id: str, data: CameraUpdateSchema, user_id=Depends(get_current_user)):
    camera = camera_controller.update(camera_id, data, user_id)
    return {"status": 200, "success": True, "message": "camera updated successfully", "data": camera}


@camera_router.delete("/{shop_id}/{camera_id}", response_model=CameraResponseModel)
def delete(shop_id: str, camera_id: str, user_id=Depends(get_current_user)):
    camera = camera_controller.delete(shop_id, camera_id, user_id)
    return {"status": 200, "success": True, "message": "camera deleted successfully", "data": camera}


@camera_router.get("/{shop_id}/{camera_id}", response_model=CameraResponseModel)
def get(shop_id: str, camera_id: str, user_id=Depends(get_current_user)):
    camera = camera_controller.get(shop_id, camera_id, user_id)
    return {"status": 200, "success": True, "message": "camera fetched successfully", "data": camera}
