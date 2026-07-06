from datetime import datetime
from typing import Literal, Optional, Annotated, Union

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class AgentConfig(BaseModel):
    agent_id: Optional[str] = None
    token: Optional[str] = None


class PublicRTSPConfig(BaseModel):
    host: str = Field(..., min_length=3, max_length=255)
    port: int = Field(..., gt=0, le=65535)
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100, exclude=True)

    device_brand: Optional[str] = Field(None, max_length=50)
    device_model: Optional[str] = Field(None, max_length=100)

    stream_path: str = Field(..., min_length=1, max_length=255)


class StreamPushConfig(BaseModel):
    push_url: str = Field(..., min_length=5, max_length=500)


ConnectionConfig = Union[
    AgentConfig,
    PublicRTSPConfig,
    StreamPushConfig
]


class Base(BaseModel):

    shop_id: PyObjectId

    type: Literal[
        "agent",
        "public_rtsp",
        "stream_push",
        "pending"
    ] = "pending"

    status: Literal[
        "connecting",
        "connected",
        "disconnected",
        "error"
    ] = "connecting"

    config: Optional[ConnectionConfig] = None

    is_active: bool = True
    soft_delete: bool = False


class Create(Base):

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)



class Update(BaseModel):

    type: Optional[
        Literal[
            "agent",
            "public_rtsp",
            "stream_push"
        ]
    ] = None

    status: Optional[
        Literal[
            "pending",
            "connecting",
            "connected",
            "disconnected",
            "error"
        ]
    ] = None

    config: Optional[ConnectionConfig] = None

    is_active: Optional[bool] = None

    soft_delete: Optional[bool] = None

    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Return(Base):

    id: PyObjectId = Field(validation_alias="_id")

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class Response(BaseModel):

    success: bool

    status: int

    message: str

    data: Optional[Return] = None