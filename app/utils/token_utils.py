import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.error_handler.custom_exception import CustomException
from app.config.environment_config import environment


def create_access_token(id: str):
    try:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {"sub": id, "iat": datetime.now(timezone.utc), "exp": expire}

        encoded_jwt = jwt.encode(payload, environment.SECRET_KEY, algorithm=environment.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise CustomException(f"something went wrong :{e}", 500)


def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(
            token, environment.SECRET_KEY, algorithms=[environment.ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError as e:
        raise CustomException(f"Token expired : {e}", 401)
    except jwt.InvalidTokenError as e:
        raise CustomException(f"Token invalid : {e}", 401)
