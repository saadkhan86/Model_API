from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Literal, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class CameraAuthSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class CameraBaseSchema(BaseModel):
    shop_id: PyObjectId
    name: str
    stream_url: str
    ip_address: str
    port: int
    auth: Optional[CameraAuthSchema] = None
    location: str
    status: Literal["online", "offline"] = "online"
    is_active: bool = True
    ai_enabled: bool = True


class CameraCreateSchema(CameraBaseSchema):
    pass


class CameraUpdateSchema(BaseModel):
    shop_id: PyObjectId
    status: Optional[Literal["online", "offline"]] = None
    is_active: Optional[bool] = None
    ai_enabled: Optional[bool] = None
    auth: Optional[CameraAuthSchema] = None
    name: Optional[str] = None
    stream_url: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    location: Optional[str] = None


class CameraResponseSchema(CameraBaseSchema):
    id: PyObjectId = Field(validation_alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attribute=True)


class CameraResponseModel(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[CameraResponseSchema] = None
