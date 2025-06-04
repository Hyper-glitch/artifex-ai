from functools import wraps

from dialogs import NOT_AUTH_MESSAGE
from telebot.types import Message


def requires_auth(handler):
    @wraps(handler)
    async def wrapper(self, message: Message, *args, **kwargs):
        try:
            await self._client.auth_user(message)
        except Exception:
            await self.bot.send_message(message.chat.id, NOT_AUTH_MESSAGE)
            return

        return await handler(self, message, *args, **kwargs)

    return wrapper
