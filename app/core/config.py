from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TASKFORCE_")

    STORAGE_PATH: Path = Path("storage/tasks.json")
    CORS_ORIGINS: str = "http://localhost:3000"
    ENV: str = "development"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
