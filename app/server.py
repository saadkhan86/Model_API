from app.router.router import router
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from app.error_handler.custom_exception import CustomException
from app.error_handler.error_handler import validation_exception_handler, http_exception_handler, custom_error_handler
app = FastAPI(title="All Routes")
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomException, custom_error_handler)


@app.get("/")
def test():
    return {"message": "Server is runnning"}


app.include_router(router)
