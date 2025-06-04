from datetime import datetime

from pydantic.v1 import Field
from typing import Literal

from enums import TaskStatus
from pydantic import BaseModel, ConfigDict


class AITaskRequest(BaseModel):
    user_id: int
    task_id: str = Field(..., description="Уникальный идентификатор задачи")
    prompt: str = Field(..., description="Исходный текст запроса для генерации изображения")
    status: Literal["new", "queued", "processing", "completed", "failed"] = Field(
        ..., description="Статус задачи"
    )
    created_at: datetime = Field(..., description="Дата создания задачи")


class MLTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: int
    model_name: str
    input_data: str
    status: TaskStatus
    created_at: datetime
    completed_at: datetime | None = None
    cost: float
    result: str | None = None


class UpdateTaskStatusRequest(BaseModel):
    task_id: str
    status: TaskStatus


class UpdateTaskResponse(BaseModel):
    task_id: str
    status: str = "success"


class UpdateTaskRequest(BaseModel):
    task_id: str
    status: TaskStatus
    result: str | None
