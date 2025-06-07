import json

import numpy as np
from aiohttp import ClientSession, FormData
from PIL import Image
import io


class TgBotClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._session = ClientSession()

    async def send_photo(self, chat_id: int, image_np: np.ndarray, task_id: str) -> None:
        form = self._prepare_form_data(chat_id, image_np, task_id)

        async with self._session.post(f"{self._base_url}/sendPhoto", data=form) as resp:
            resp.raise_for_status()

    async def send_error_msg(self, chat_id: int) -> None:
        payload = {
            "chat_id": chat_id,
            "text": "⚠️ Упс, произошла ошибка. Попробуйте еще раз.",
            "parse_mode": "Markdown",
        }
        async with self._session.post(f"{self._base_url}/sendMessage", json=payload) as resp:
            resp.raise_for_status()

    def _prepare_form_data(self, chat_id: int, image_np: np.ndarray, task_id: str) -> FormData:
        form = FormData()
        form.add_field("chat_id", str(chat_id))
        form.add_field("caption", "Оцените результат работы нейросети от 1 до 5.")
        form.add_field(
            "photo",
            self._prepare_image(image_np),
            filename="image.png",
            content_type="image/png",
        )
        reply_markup = {
            "inline_keyboard": [
                [{"text": f"{i} ⭐", "callback_data": f"rate_{i}|{task_id}"} for i in range(1, 6)]
            ]
        }
        form.add_field("reply_markup", json.dumps(reply_markup))

        return form

    @staticmethod
    def _prepare_image(image_np: np.ndarray) -> bytes:
        """Convert image from np type to bytes."""
        image = Image.fromarray(image_np)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        return buffer.getvalue()
