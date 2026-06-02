from pydantic import BaseModel, EmailStr, BeforeValidator, Field, ConfigDict
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Base(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class Signup(Base):
    password: str = Field(..., min_length=6)


class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class Update(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=20)


class Return(Base):
    id: PyObjectId = Field(validation_alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class Response(BaseModel):
    status: int
    success: bool
    message: str
    data: Optional[Return] = None
