import app.controller.user_controller as user_controller
from app.schema.user_schema import Response, Signup, Login, Update
import app.utils.token_utils as jwt
from fastapi import APIRouter, status, Depends
from app.middlewares.authenticate_user import get_current_user

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Response)
def signup(data: Signup):
    user_controller.signup(data)
    return {"status": 201, "success": True, "message": "user created successfully"}


@user_router.post("/login", response_model=dict)
def login(data: Login):
    user = user_controller.login(data)
    return {"status": 200, "success": True, "message": "user logged in successfully", "data": user}


@user_router.get("/",  response_model=Response)
def get(id: str = Depends(get_current_user)):
    user = user_controller.get(id)
    return {"status": 200, "success": True, "message": "user fetched successfully", "data": user}


@user_router.patch("/", response_model=Response)
def update(user: Update, id: str = Depends(get_current_user)):
    user = user_controller.update(id, user)
    return {"status": 200, "success": True, "message": "user updated successfully", "data": user}


@user_router.delete("/", response_model=Response)
def delete(id: str = Depends(get_current_user)):
    user_controller.delete(id)
    return {"status": 200, "success": True, "message": "user deleted successfully"}
