from functools import wraps
from fastapi import status
from app.error_handler.custom_exception import CustomException


def error_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(
                f"internal server error: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
