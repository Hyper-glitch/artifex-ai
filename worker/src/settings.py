from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    BASE_API_URL: str = "http://0.0.0.0:8080/api/v1"
    API_AUTH_TOKEN: str
    TG_BOT_TOKEN: str

    RABBITMQ_DEFAULT_USER: str = "admin"
    RABBITMQ_DEFAULT_PASS: str = "admin"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_HEARTBEAT: int = 30
    RABBITMQ_QUEUE_NAME: str = "gen-ai-tasks"

    TRITON_MAX_CONCURRENCY: int = 1
    TRITON_MODEL_NAME: str = "artifex-ai.main"
    TRITON_CLIENT_URL: str = "http://localhost:8000"

    GEN_IMAGE_WIDTH: int = 512
    GEN_IMAGE_HEIGHT: int = 512

    @property
    def rmq_url(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/%2F"
        )


settings = Settings()
