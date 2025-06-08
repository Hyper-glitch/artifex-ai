from client import AsyncApiClient
from decorator import requires_auth
from dialogs import (
    ASK_NEW_PROMPT_MESSAGE,
    ERROR_MESSAGE,
    PROCESSING_MESSAGE,
    RATE_THANKS_MESSAGE,
    STATUS_MESSAGES,
    START_MESSAGE,
    ERROR_TASK_MESSAGE,
    AWAITING_PROMPT_MESSAGE,
)
from loguru import logger
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message


class Handlers:
    _user_states: dict[int, str] = {}

    def __init__(self, bot: AsyncTeleBot, client: AsyncApiClient) -> None:
        self.bot = bot
        self._client = client

        self.bot.message_handler(commands=["start"])(self.start_handler)
        self.bot.message_handler(commands=["generate"])(self.handle_generate_command)
        self.bot.message_handler(commands=["registrate"])(self.handle_registrate)
        self.bot.message_handler(content_types=["text"])(self.handle_prompt)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("rate_"))(
            self.callback_handler
        )

    async def start_handler(self, message: Message) -> None:
        await self.bot.send_message(message.chat.id, START_MESSAGE)

    async def handle_registrate(self, message: Message) -> None:
        try:
            status = await self._client.sign_up(message)
        except Exception as exc:
            logger.error(f"Problem when sign up user in API. {exc}")
            await self.bot.send_message(message.chat.id, ERROR_MESSAGE)
            return

        await self.bot.send_message(
            chat_id=message.chat.id,
            text=STATUS_MESSAGES.get(status, ERROR_MESSAGE),
        )

    @requires_auth
    async def handle_generate_command(self, message: Message):
        await self.bot.send_message(message.chat.id, AWAITING_PROMPT_MESSAGE)
        self._user_states[message.chat.id] = "awaiting_prompt"

    @requires_auth
    async def handle_prompt(self, message: Message):
        state = self._user_states.get(message.chat.id)

        if state == "awaiting_prompt":
            try:
                await self._client.create_task(message)
            except Exception as exc:
                logger.exception(f"Task creation failed. Error: {exc}")
                await self.bot.send_message(message.chat.id, ERROR_TASK_MESSAGE)
            else:
                self._user_states.pop(message.chat.id, None)
                await self.bot.send_message(message.chat.id, PROCESSING_MESSAGE)

    @requires_auth
    async def callback_handler(self, call: CallbackQuery) -> None:
        _, payload = call.data.split("rate_")
        rating_str, task_id = payload.split("|")
        rating = int(rating_str)

        await self._client.create_feedback(
            rating=rating,
            task_id=task_id,
        )
        await self.bot.send_message(call.message.chat.id, RATE_THANKS_MESSAGE)
        self._user_states[call.message.chat.id] = "awaiting_prompt"

        await self.bot.send_message(call.message.chat.id, ASK_NEW_PROMPT_MESSAGE)
