from buttons import create_rating_buttons, create_action_buttons
from client import AsyncApiClient
from dialogs import (
    ACCEPTED_MESSAGE,
    ASK_NEW_PROMPT_MESSAGE,
    PROCESSING_MESSAGE,
    REGENERATING_MESSAGE,
    START_MESSAGE, ERROR_MESSAGE, RATE_PROMPT_MESSAGE, RATE_THANKS_MESSAGE,
)
from enums import CallbackData
from loguru import logger
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message


class Handlers:
    def __init__(self, bot: AsyncTeleBot, client: AsyncApiClient) -> None:
        self.bot = bot
        self._client = client

        self.bot.message_handler(commands=["start"])(self.start_handler)
        self.bot.message_handler(content_types=["text"])(self.task_handler)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_handler)

    async def start_handler(self, message: Message) -> None:
        await self.bot.send_message(message.chat.id, START_MESSAGE)

    async def task_handler(self, message: Message) -> None:
        logger.info("Starting to process user prompt...")
        await self.bot.send_message(message.chat.id, PROCESSING_MESSAGE)
        try:
            await self._client.create_task(message)
        except Exception as exc:
            logger.error(f"Problem when creating task in API. {exc}")
            await self.bot.send_message(message.chat.id, ERROR_MESSAGE)

        await self.bot.send_message(message.chat.id, "DONE", reply_markup=create_action_buttons())

    async def callback_handler(self, call: CallbackQuery) -> None:
        if call.data == CallbackData.ACCEPT:
            await self.bot.answer_callback_query(call.id, ACCEPTED_MESSAGE)
            await self.bot.send_message(call.message.chat.id, RATE_PROMPT_MESSAGE, reply_markup=create_rating_buttons())

        elif call.data == CallbackData.REGENERATE:
            await self.bot.answer_callback_query(call.id, REGENERATING_MESSAGE)

        elif call.data.startswith("rate_"):
            await self._client.create_feedback(
                user_id=call.from_user.id,
                rating=int(call.data.split("_")[1]),
            )
            await self.bot.send_message(call.message.chat.id, RATE_THANKS_MESSAGE)
            await self.bot.send_message(call.message.chat.id, ASK_NEW_PROMPT_MESSAGE)
