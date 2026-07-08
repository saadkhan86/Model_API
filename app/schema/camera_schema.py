from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Literal, Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Base(BaseModel):
    shop_id: PyObjectId

    name: str = Field(..., min_length=3, max_length=100)

    channel_no: int = Field(..., ge=1)

    location: Optional[str] = Field(None, min_length=3, max_length=255)

    status: Literal[
        "online",
        "offline",
        "error"
    ] = "offline"

    ai_enabled: bool = False

    engine_id: Optional[str] = None

    last_seen: Optional[datetime] = None

    soft_delete: bool = False


class Create(Base):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Update(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)

    channel_no: Optional[int] = Field(None, ge=1)

    location: Optional[str] = Field(None, min_length=3, max_length=255)

    status: Optional[
        Literal[
            "online",
            "offline",
            "error"
        ]
    ] = None

    ai_enabled: Optional[bool] = None

    engine_id: Optional[str] = None

    last_seen: Optional[datetime] = None

    soft_delete: Optional[bool] = None

    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Return(Base):
    id: PyObjectId = Field(validation_alias="_id")

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attribute=True
    )


class Response(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Return] = None