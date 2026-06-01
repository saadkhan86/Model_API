from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.token_utils import decode_access_token
from app.repositories.UsersRepo import UsersRepo
from app.error_handler.custom_exception import CustomException
oauth2_scheme = HTTPBearer()
users_repo = UsersRepo()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise CustomException("Token invalid", status.HTTP_401_UNAUTHORIZED)
    user = users_repo.get_user_by_id(payload.get("sub"))
    if not user:
        raise CustomException("user not found", status.HTTP_404_NOT_FOUND)
    return str(user.id)
