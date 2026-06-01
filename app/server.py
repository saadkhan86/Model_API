from app.router.router import router
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from contextlib import asynccontextmanager
from app.error_handler.custom_exception import CustomException
from app.error_handler.error_handler import *
from app.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting -----> establishing database")
    init_db()
    yield
    print("server is going to stop -------> closing database")


app = FastAPI(title="All Routes", lifespan=lifespan)


@app.get("/")
def test():
    return {"message": "Server is runnning"}


app.include_router(router)

app.add_exception_handler(CustomException, custom_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
