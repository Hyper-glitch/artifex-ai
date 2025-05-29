from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "artifex-ai-api-service"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    AUTH_TOKEN: str = ""
    ANALYTICS_API_KEY: str = ""

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "database"

    RABBITMQ_DEFAULT_USER: str = "admin"
    RABBITMQ_DEFAULT_PASS: str = "admin"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_HEARTBEAT: int = 30
    RABBITMQ_QUEUE_NAME: str = "gen-ai-tasks"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def rmq_url(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/%2F"
        )


settings = Settings()
