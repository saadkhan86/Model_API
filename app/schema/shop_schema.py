from datetime import datetime
from typing import Literal, Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class Base(BaseModel):
    owner_id: PyObjectId
    name: str = Field(..., min_length=3, max_length=100)
    branch_name: Optional[str] = Field(None, min_length=3, max_length=100)
    country: str = Field(..., min_length=2, max_length=50)
    city: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=3, max_length=255)
    timezone: str = Field(default="Asia/Karachi", max_length=50)
    status: Literal["active", "inactive"] = "active"
    soft_delete: bool = False

class Create(Base):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Update(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    branch_name: Optional[str] = Field(None, min_length=3, max_length=100)
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=3, max_length=255)
    timezone: Optional[str] = Field(None, max_length=50)
    status: Optional[Literal["active", "inactive"]] = None

class Return(Base):
    id: PyObjectId = Field(validation_alias="_id")
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class Response(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Return] = None

class ListResponse(BaseModel):
    success: bool
    status: int
    message: str
    data: list[Return] = []