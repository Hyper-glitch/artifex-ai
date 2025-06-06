from pydantic import BaseModel


class TaskOutput(BaseModel):
    prediction: float


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
