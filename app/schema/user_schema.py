from pydantic import BaseModel, EmailStr, BeforeValidator, Field
from typing import Optional, Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserSignUpSchema(UserBaseSchema):
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponseSchema(UserBaseSchema):
    id: PyObjectId = Field(alias="_id")
