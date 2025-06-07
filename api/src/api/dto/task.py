from datetime import datetime

from pydantic.v1 import Field
from typing import Literal

from enums import TaskStatus
from pydantic import BaseModel


class AITaskRequest(BaseModel):
    user_id: int
    task_id: str = Field(..., description="Уникальный идентификатор задачи")
    prompt: str = Field(..., description="Исходный текст запроса для генерации изображения")
    status: Literal["new", "queued", "processing", "completed", "failed"] = Field(
        ..., description="Статус задачи"
    )
    chat_id: int
    created_at: datetime = Field(..., description="Дата создания задачи")


class UpdateTaskStatusRequest(BaseModel):
    task_id: str
    status: TaskStatus


class UpdateTaskRequest(BaseModel):
    task_id: str
    rating: int | None = Field(None, ge=0, le=5)
    status: TaskStatus | None = None
    logs: str | None = None
