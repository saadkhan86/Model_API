from pydantic import BaseModel
from typing import Literal, Optional


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
    id: str
    user_id: str
