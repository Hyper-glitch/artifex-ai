import logging

import numpy as np

from clients.atrifex import AsyncApiClient
from clients.tg_bot import TgBotClient
from clients.triton import AsyncTritonClient
from dto import RMQMessage
from enums import TaskStatus


class GenAIProcessingService:
    def __init__(
        self, api_cleint: AsyncApiClient, triton_client: AsyncTritonClient, tg_bot: TgBotClient
    ) -> None:
        self._client = api_cleint
        self._triton_client = triton_client
        self._tg_bot = tg_bot

    async def process_task(self, msg: RMQMessage) -> None:
        logging.info(f"Starting to process genAI task {msg.task_id}...")
        await self._safe_update_status(msg.task_id, TaskStatus.PROCESSING)

        try:
            image_np = await self._triton_client.infer(msg)
        except Exception as exc:
            await self._safe_update_status(
                msg.task_id, TaskStatus.FAILED, detail=f"Inference failed: {exc}"
            )
            logging.error(f"ML inference failed for task {msg.task_id}: {exc}")
            return

        await self._safe_update_status(
            msg.task_id, TaskStatus.COMPLETED, detail="Inference successful"
        )
        await self._safe_send_photo(msg.chat_id, image_np, caption="Вот ваше изображение")
        logging.info(f"GenAI task - {msg.task_id} - successfully processed.")

    async def _safe_update_status(
        self, task_id: str, status: TaskStatus, detail: str | None = None
    ) -> None:
        try:
            await self._client.update_task(task_id=task_id, status=status, detail=detail)
        except Exception as exc:
            logging.error(f"Failed to update status {status} for task {task_id}: {exc}")

    async def _safe_send_photo(self, chat_id: int | str, image_np: np.ndarray, caption: str) -> None:
        try:
            await self._tg_bot.send_photo(chat_id=chat_id, image_np=image_np, caption=caption)
        except Exception as exc:
            logging.error(f"Failed to send photo to chat {chat_id}: {exc}")
