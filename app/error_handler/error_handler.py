from fastapi import Request, status
from fastapi.responses import JSONResponse
from .custom_exception import CustomException


def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code or 500,
        content={"message": exc.detail or "Internal server error",
                 "success": False, "data": None},
    )


def validation_exception_handler(request: Request, exc: HTTPException):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": error["loc"][0],
            "message": error["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation Failed!",
                 "success": False, "errors": errors}
    )


def custom_error_handler(request: Request, exc: CustomException):
    return JSONResponse(status_code=exc.status_code, content={"success": False, "status": exc.status_code, "message": exc.message, "data": None})
