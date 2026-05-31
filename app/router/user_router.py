import app.controller.user_controller as user_controller
from app.schema.user_schema import *
import app.utils.token_utils as jwt
from fastapi import APIRouter, status, Depends, HTTPException
from app.middlewares.authenticate_user import get_current_user

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel)
def signup_user(data: UserSignUpSchema):
    user = user_controller.signup_user(data)
    return {"status": 201, "success": True, "message": "user created successfully"}


@user_router.post("/login")
async def login_user(data: UserLoginSchema):
    user = user_controller.login_user(data)
    return {"status": 200, "success": True, "message": "user loggedin successfully", "data": user}


@user_router.get("/{id}",  response_model=UserResponseModel)
async def get_user_by_id(id: str, get_current_user_id=Depends(get_current_user)):
    if id != get_current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user = user_controller.get_user_by_id(id)
    return {"status": 200, "success": True, "message": "user fetched successfully", "data": user}


@user_router.put("/{id}",  response_model=UserResponseModel)
def update_user(id: str, user: UserUpdateSchema, get_current_user_id=Depends(get_current_user)):
    if id != get_current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user = user_controller.update_user(get_current_user_id, user)
    return {"status": 200, "success": True, "message": "user updated successfully", "data": user}


@user_router.delete("/{id}", response_model=UserResponseModel)
def delete_user(id: str, get_current_user_id=Depends(get_current_user)):
    if id != get_current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    user = user_controller.delete_user(get_current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"status": 200, "success": True, "message": "user deleted successfully"}
