from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Literal, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Auth(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    password: Optional[str] = Field(
        None, min_length=6, max_length=20, exclude=True)


class Base(BaseModel):
    shop_id: PyObjectId
    name: str = Field(..., min_length=3, max_length=50)
    stream_url: str = Field(..., min_length=3, max_length=255)
    ip_address: str = Field(..., min_length=3, max_length=255)
    port: int = Field(..., gt=0, le=65535)
    location: str = Field(..., min_length=3, max_length=255)
    auth: Optional[Auth] = None
    status: Literal["online", "offline"] = "online"
    is_active: bool = True
    ai_enabled: bool = True


class Create(Base):
    pass


class Update(BaseModel):
    shop_id: PyObjectId
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    stream_url: Optional[str] = Field(None, min_length=3, max_length=255)
    ip_address: Optional[str] = Field(None, min_length=3, max_length=255)
    port: Optional[int] = Field(None, gt=0, le=65535)
    location: Optional[str] = Field(None, min_length=3, max_length=255)
    auth: Optional[Auth] = None
    status: Optional[Literal["online", "offline"]] = None
    is_active: Optional[bool] = None
    ai_enabled: Optional[bool] = None


class Return(Base):
    id: PyObjectId = Field(validation_alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attribute=True)


class Response(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Return] = None
