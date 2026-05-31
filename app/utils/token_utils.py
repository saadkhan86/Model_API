import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
SECRET_KEY = "kdsfksjfksdjfkieyurfwe1dfgfggdfgdferertdfcbvbcdhfghfg234567890abc"
ALGORITHM = "HS256"


def create_access_token(id: str):
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    payload = {"sub": id, "iat": datetime.now(timezone.utc), "exp": expire}

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        print(f"[DEBUG] Token repr: {repr(token)}")  # shows hidden chars
        clean_token = str(token).strip()
        decoded_token = jwt.decode(
            clean_token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid"
        )
