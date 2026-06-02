from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class EnvironmentSchema(BaseSettings):
    MONGO_DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


