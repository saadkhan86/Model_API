from pwdlib import PasswordHash
from app.error_handler.custom_exception import CustomException
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    try:
        return password_hash.hash(password)
    except Exception as e:
        raise CustomException(f"Something went wrong in hashing: {e}", 500)


def verify_password(oldPassword: str, newPassword: str) -> bool:
    try:
        return password_hash.verify(newPassword, oldPassword)
    except Exception as e:
        raise CustomException(f"Something went wrong in verifying password : {e}", 500)
