from app.utils.hash_helper import hash_password, verify_password
from app.utils.token_utils import create_access_token
from app.schema.user_schema import Signup, Login, Update
from app.error_handler.custom_exception import CustomException
from app.utils.error_wrapper import error_wrapper
from app.repositories.UsersRepo import UsersRepo

users_repo = UsersRepo()


@error_wrapper
def signup(user: Signup):
    existing_user = users_repo.get_by_email(user.email)
    if existing_user:
        raise CustomException("User already exists", 409)
    user.password = hash_password(user.password)
    return users_repo.signup(user)


@error_wrapper
def login(user:Login):
    existing_user = users_repo.get_by_email(user.email)
    if not existing_user:
        raise CustomException("User not found", 404)
    if not verify_password(existing_user["password"], user.password):
        raise CustomException("Incorrect password", 401)
    return create_access_token(str(existing_user["_id"]))


@error_wrapper
def update(user_id: str, data: Update):
    if data.password:
        data.password = hash_password(data.password)
    return users_repo.update(user_id, data)


@error_wrapper
def delete(user_id: str):
    return users_repo.delete(user_id)


@error_wrapper
def get(user_id: str):
    return users_repo.get(user_id)
