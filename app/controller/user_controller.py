from app.models.users_model import *
from app.schema.user_schema import *
from app.utils.hash_helper import *
from app.utils.token_utils import create_access_token
from app.error_handler.custom_exception import *
from app.utils.error_wrapper import *


@error_wrapper
def signup_user(user: UserSignUpSchema):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise CustomException("user already exists", 409)
    user.password = hash_password(user.password)
    user = create_user(user)
    return user


@error_wrapper
def login_user(user: UserLoginSchema):
    existing_user = get_user_by_email(user.email)
    if not existing_user:
        raise CustomException("user not found", 404)
    if not verify_password(existing_user["password"], user.password):
        raise CustomException("incorrect password", 401)
    token = create_access_token(str(existing_user["_id"]))
    return token


@error_wrapper
def update_user(user_id: str, data: UserUpdateSchema):
    user = update_user_by_id(user_id, data)
    if not user:
        raise CustomException("user not found", 404)
    return user


@error_wrapper
def delete_user(user_id: str):
    return delete_user_by_id(user_id)


@error_wrapper
def get_user(user_id: str):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise CustomException("User not found", 404)
    return existing_user
