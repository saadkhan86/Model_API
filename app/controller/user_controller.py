from app.utils.hash_helper import hash_password, verify_password
from app.utils.token_utils import create_access_token
from app.schema.user_schema import UserSignUpSchema, UserLoginSchema, UserUpdateSchema
from app.error_handler.custom_exception import CustomException
from app.utils.error_wrapper import error_wrapper
from app.repositories.UsersRepo import UsersRepo

users_repo = UsersRepo()


@error_wrapper
def signup_user(user: UserSignUpSchema):
    existing_user = users_repo.get_user_by_email(user.email)
    if existing_user:
        raise CustomException("User already exists", 409)
    user.password = hash_password(user.password)
    return users_repo.create_user(user)


@error_wrapper
def login_user(user: UserLoginSchema):
    existing_user = users_repo.get_user_by_email(user.email)
    if not existing_user:
        raise CustomException("User not found", 404)
    if not verify_password(existing_user["password"], user.password):
        raise CustomException("Incorrect password", 401)
    return create_access_token(str(existing_user["_id"]))


@error_wrapper
def update_user(user_id: str, data: UserUpdateSchema):
    return users_repo.update_user(user_id, data)


@error_wrapper
def delete_user(user_id: str):
    return users_repo.delete_user(user_id)


@error_wrapper
def get_user(user_id: str):
    return users_repo.get_user_by_id(user_id)
