from pydantic import BaseModel, Field

from enums import TaskStatus


class Inputs(BaseModel):
    name: str = "prompt"
    shape: list[int] = [1]
    datatype: str = "BYTES"
    data: list[str]


class TritonInput(BaseModel):
    inputs: list[Inputs]


class RMQMessage(BaseModel):
    task_id: str
    prompt: str
    chat_id: int


class UpdateTaskRequest(BaseModel):
    task_id: str
    rating: int | None = Field(default=None, ge=0, le=5)
    status: TaskStatus | None = None
    logs: str | None = None
