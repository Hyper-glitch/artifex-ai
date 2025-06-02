from datetime import datetime

from enums import TaskStatus
from pydantic import BaseModel, ConfigDict


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
