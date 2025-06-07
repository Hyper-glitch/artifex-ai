from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class BaseUserInfo(BaseModel):
    id: int = Field(..., description="Уникальный Telegram user_id")
    username: str | None = Field(None, description="Telegram username")


class AuthUserRequest(BaseUserInfo):
    pass


class AuthUserResponse(BaseModel):
    success: bool
    message: str


class UserInfo(BaseUserInfo):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str | None = Field(None, description="Фамилия пользователя")
    language_code: str | None = Field(None, description="Код языка, например 'ru', 'en'")


class UpdateTaskRequest(BaseModel):
    task_id: str
    rating: int | None = Field(default=None, ge=0, le=5)


class CreateTaskRequest(BaseModel):
    user_id: int
    task_id: str = Field(..., description="Уникальный идентификатор задачи")
    prompt: str = Field(..., description="Исходный текст запроса для генерации изображения")
    status: Literal["new", "queued", "processing", "completed", "failed"] = Field(
        "new", description="Статус задачи"
    )
    chat_id: int
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Дата создания задачи"
    )
