import uuid
from urllib.parse import urljoin

from aiohttp import ClientSession
from schemas import (
    AuthUserRequest,
    CreateTaskRequest,
    UpdateTaskRequest,
    UserInfo,
)
from telebot.types import Message
from loguru import logger


class AsyncApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._session = self._create_session(token, base_url)

    async def sign_in(self, message: Message) -> None:
        dto = AuthUserRequest.model_validate(message.from_user.to_dict())
        async with self._session.post("users/sign-in/", json=dto.model_dump()) as resp:
            resp.raise_for_status()

    async def sign_up(self, message: Message) -> int:
        dto = UserInfo.model_validate(message.json["chat"])
        async with self._session.post("users/sign-up/", json=dto.model_dump()) as resp:
            return resp.status

    async def create_task(self, message: Message) -> None:
        dto = CreateTaskRequest(
            user_id=message.from_user.id,
            task_id=str(uuid.uuid4()),
            chat_id=message.chat.id,
            prompt=message.text,
        )
        async with self._session.post("tasks/create/", json=dto.model_dump(mode="json")) as resp:
            resp.raise_for_status()

        logger.info(f"Task {dto.task_id} created successfully.")

    async def create_feedback(self, rating: int, task_id: str) -> None:
        dto = UpdateTaskRequest(task_id=task_id, rating=rating)
        async with self._session.post("tasks/update/", json=dto.model_dump()) as resp:
            resp.raise_for_status()

    @staticmethod
    def _create_session(token: str, base_url: str) -> ClientSession:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        return ClientSession(headers=headers, base_url=urljoin(base_url, "/api/v1/"))
