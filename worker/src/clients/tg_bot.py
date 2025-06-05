import base64
from aiohttp import ClientSession, FormData


class TgBotClient:
    def __init__(self, token: str) -> None:
        self._token = token
        self._base_url = f"https://api.telegram.org/bot{token}"
        self._session = ClientSession()

    async def send_photo(
        self, chat_id: int | str, image_data: str, caption: str = "", filename: str = "image.png"
    ) -> None:
        form = FormData()
        form.add_field("chat_id", str(chat_id))
        form.add_field("caption", caption)
        form.add_field(
            "photo",
            base64.b64decode(image_data),
            filename=filename,
            content_type="image/png",
        )

        async with self._session.post(f"{self._base_url}/sendPhoto", data=form) as resp:
            resp.raise_for_status()

    async def close(self) -> None:
        await self._session.close()
