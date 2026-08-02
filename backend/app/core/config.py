from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LexPilot AI"
    environment: str = "development"
    database_url: str = "sqlite:///./lexpilot.db"
    upload_dir: Path = Path("uploads")
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    max_upload_mb: int = 25
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
