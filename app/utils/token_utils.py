import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.error_handler.custom_exception import CustomException
SECRET_KEY = "kdsfksjfksdjfkieyurfwe1dfgfggdfgdferertdfcbvbcdhfghfg234567890abc"
ALGORITHM = "HS256"


def create_access_token(id: str):
    try:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {"sub": id, "iat": datetime.now(timezone.utc), "exp": expire}

        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise CustomException(f"something went wrong :{e}", 500)


def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError as e:
        raise CustomException(f"Token expired : {e}", 401)
    except jwt.InvalidTokenError as e:
        raise CustomException(f"Token invalid : {e}", 401)
