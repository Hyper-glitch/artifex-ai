import numpy as np
from aiohttp import ClientSession, FormData
from PIL import Image
import io


class TgBotClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._session = ClientSession()

    async def send_photo(
        self, chat_id: int, image_np: np.ndarray, caption: str = "", filename: str = "image.png"
    ) -> None:
        form = FormData()
        form.add_field("chat_id", str(chat_id))
        form.add_field("caption", caption)
        form.add_field(
            "photo",
            self._prepare_image(image_np),
            filename=filename,
            content_type="image/png",
        )

        async with self._session.post(f"{self._base_url}/sendPhoto", data=form) as resp:
            resp.raise_for_status()

    @staticmethod
    def _prepare_image(image_np: np.ndarray) -> bytes:
        """Convert image from np type to bytes."""
        image = Image.fromarray(image_np)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        return buffer.getvalue()

    async def close(self) -> None:
        await self._session.close()
