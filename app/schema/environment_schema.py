from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class EnvironmentSchema(BaseSettings):
    MONGO_DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")
