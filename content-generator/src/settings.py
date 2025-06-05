import logging
from typing import ClassVar, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from ttk import Venv


logging.basicConfig(level=logging.INFO)
Venv.set_default_version("24.06")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DEPLOYMENT_GROUP: ClassVar[str] = "content-generator"
    DEPLOYMENT_VERSION: ClassVar[int] = 1

    MLFLOW_TRACKING_URL: str = "http://localhost:8008"
    MLFLOW_TRACKING_USERNAME: str = ""
    MLFLOW_TRACKING_PASSWORD: str = ""

    SOURCE_REPOSITORY_URL: str
    SOURCE_REPOSITORY_ACCESS_KEY_ID: str
    SOURCE_REPOSITORY_SECRET_ACCESS_KEY: str
    SOURCE_REPOSITORY_BUCKET: str
    SOURCE_REPOSITORY_PREFIX: str

    TRITON_CLIENT_URL: str = "http://localhost:8000"
    TRITON_CLIENT_VERIFY_TLS: bool = True
    TRITON_REPOSITORY_URL: str = "http://localhost:9000"
    TRITON_REPOSITORY_ACCESS_KEY_ID: str = "minioadmin"
    TRITON_REPOSITORY_SECRET_ACCESS_KEY: str = "minioadmin"
    TRITON_REPOSITORY_BUCKET: str
    TRITON_REPOSITORY_PREFIX: str
    TRITON_REPOSITORY_RELOAD_POLICY: Literal["none", "restart", "rollout"] = "none"


settings = Settings()
