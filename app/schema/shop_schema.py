from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Literal, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Base(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=3, max_length=255)
    status: Literal["active", "inactive"] = "active"


class Create(Base):
    pass


class Update(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    address: Optional[str] = Field(None, min_length=3, max_length=255)
    status: Optional[Literal["active", "inactive"]] = None


class Return(Base):
    id: PyObjectId = Field(validation_alias="_id")
    user_id: Optional[PyObjectId] = None

    model_config = ConfigDict(populate_by_name=True, from_attribute=True)


class Response(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Return] = None
