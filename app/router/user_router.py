import app.controller.user_controller as user_controller
from app.schema.user_schema import UserResponseModel, UserSignUpSchema, UserLoginSchema, UserUpdateSchema
import app.utils.token_utils as jwt
from fastapi import APIRouter, status, Depends
from app.middlewares.authenticate_user import get_current_user

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel)
def signup_user(data: UserSignUpSchema):
    user_controller.signup_user(data)
    return {"status": 201, "success": True, "message": "user created successfully"}


@user_router.post("/login")
def login_user(data: UserLoginSchema):
    user = user_controller.login_user(data)
    return {"status": 200, "success": True, "message": "user logged in successfully", "data": user}


@user_router.get("/",  response_model=UserResponseModel)
def get_user(id: str = Depends(get_current_user)):
    user = user_controller.get_user(id)
    return {"status": 200, "success": True, "message": "user fetched successfully", "data": user}


@user_router.put("/", response_model=UserResponseModel)
def update_user(user: UserUpdateSchema, id: str = Depends(get_current_user)):
    user = user_controller.update_user(id, user)
    return {"status": 200, "success": True, "message": "user updated successfully", "data": user}


@user_router.delete("/", response_model=UserResponseModel)
def delete_user(id: str = Depends(get_current_user)):
    user_controller.delete_user(id)
    return {"status": 200, "success": True, "message": "user deleted successfully"}
