from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    id: int = Field(..., description="Уникальный Telegram user_id")
    username: Optional[str] = Field(None, description="Telegram username")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    language_code: Optional[str] = Field(None, description="Код языка, например 'ru', 'en'")


class FeedbackTaskRequest(BaseModel):
    user_id: int = Field(..., description="Telegram user_id")
    task_id: str = Field(..., description="Уникальный идентификатор задачи/запроса")
    rating: int = Field(..., ge=1, le=5, description="Оценка качества от 1 до 5")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Время оставления отзыва"
    )


class CreateTaskRequest(BaseModel):
    user_info: UserInfo
    task_id: str = Field(..., description="Уникальный идентификатор задачи")
    prompt: str = Field(..., description="Исходный текст запроса для генерации изображения")
    status: Literal["new", "queued", "processing", "completed", "failed"] = Field(
        "new", description="Статус задачи"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Дата создания задачи"
    )
