from fastapi import Request, status
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code or 500,
        content={"message": exc.detail or "Internal server error",
                 "success": False, "data": None},
    )


async def validation_exception_handler(request: Request, exc: HTTPException):
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
