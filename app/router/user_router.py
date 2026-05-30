import app.controller.user_controller as user_controller
import app.schema.user_schema as user_schema

from fastapi import APIRouter, status

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(user: user_schema.UserSignUpSchema):
    return user_controller.signup_user(user)


@user_router.post("/login", response_model=user_schema.UserResponseSchema)
async def login_user(user: user_schema.UserLoginSchema):
    return user_controller.login_user(user)


@user_router.get("/{id}", response_model=user_schema.UserResponseSchema)
async def get_user_by_id(id: str):
    return user_controller.get_user_by_id(id)


@user_router.put("/{id}", response_model=user_schema.UserResponseSchema)
def update_user(id: str, user: user_schema.UserUpdateSchema):
    return user_controller.update_user(id, user)


@user_router.delete("/{id}")
def delete_user(id: str):
    return user_controller.delete_user(id)
