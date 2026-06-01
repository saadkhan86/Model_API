from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Literal, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class BaseShopSchema(BaseModel):
    name: str
    address: str
    status: Literal["active", "inactive"] = "active"


class ShopCreateSchema(BaseShopSchema):
    pass


class ShopUpdateSchema(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None


class ShopResponseSchema(BaseShopSchema):
    id: PyObjectId = Field(validation_alias="_id")
    user_id: Optional[PyObjectId] = None

    model_config = ConfigDict(populate_by_name=True, from_attribute=True)


class ShopResponseModel(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[ShopResponseSchema] = None
