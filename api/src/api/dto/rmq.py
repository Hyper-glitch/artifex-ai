from uuid import UUID

from pydantic import BaseModel


class RMQMessage(BaseModel):
    task_id: str
    prompt: str
    chat_id: int
