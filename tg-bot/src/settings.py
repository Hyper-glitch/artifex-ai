from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    TELEGRAM_BOT_TOKEN: str

    API_CLIENT_URL: str
    API_CLIENT_AUTH_TOKEN: str


settings = Settings()
