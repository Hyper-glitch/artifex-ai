import uuid
from telebot.types import Message

import aiohttp
from aiohttp import ClientSession
from schemas import CreateTaskRequest, UserInfo, FeedbackTaskRequest


class AsyncApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._session = self._create_session(token, base_url)

    async def create_task(self, message: Message) -> None:
        dto = CreateTaskRequest(
            user_info=UserInfo.model_validate(message.from_user.to_dict()),
            task_id=str(uuid.uuid4()),
            prompt=message.text,
        )
        async with self._session.post("/tasks/create", json=dto.model_dump()) as resp:
            resp.raise_for_status()

    async def create_feedback(self, user_id: int, rating: int) -> None:
        dto = FeedbackTaskRequest(
            user_id=user_id,
            task_id=str(uuid.uuid4()),
            rating=rating,
        )
        async with self._session.post("/feedback/create", json=dto.model_dump()) as resp:
            resp.raise_for_status()

    @staticmethod
    def _create_session(token: str, base_url: str) -> ClientSession:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        return aiohttp.ClientSession(headers=headers, base_url=base_url)
