from uuid import UUID

from pydantic import BaseModel


class RMQMessage(BaseModel):
    task_id: UUID
    user_id: int
    prompt: str
