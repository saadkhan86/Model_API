import app.models.users_model as users_model
from app.schema.user_schema import UserSignUpSchema, UserUpdateSchema, UserResponseSchema, UserLoginSchema
from fastapi import HTTPException, status


def signup_user(user: UserSignUpSchema):
    existing_user = users_model.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = users_model.create_user(user.model_dump())
    return user


def login_user(user: UserLoginSchema):
    existing_user = users_model.get_user_by_email(user.email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if existing_user["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return existing_user


def update_user(user_id: str, user: UserUpdateSchema):
    existing_user = users_model.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = users_model.update_user_by_id(
        user_id, user.model_dump(exclude_unset=True))
    updated_user = users_model.get_user_by_id(user_id)
    return updated_user


def delete_user(user_id: str):
    existing_user = users_model.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = users_model.delete_user_by_id(user_id)
    return {"message": "user deleted successfully"}


def get_user_by_id(user_id: str):
    existing_user = users_model.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return existing_user
