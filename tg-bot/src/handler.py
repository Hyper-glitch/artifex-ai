from buttons import create_action_buttons, create_rating_buttons
from client import AsyncApiClient
from decorator import requires_auth
from dialogs import (
    ACCEPTED_MESSAGE,
    ASK_NEW_PROMPT_MESSAGE,
    ERROR_MESSAGE,
    PROCESSING_MESSAGE,
    RATE_PROMPT_MESSAGE,
    RATE_THANKS_MESSAGE,
    REGENERATING_MESSAGE,
    SUCCESS_SIGN_UP,
    WELCOME_MESSAGE,
)
from enums import CallbackData
from loguru import logger
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message


class Handlers:
    def __init__(self, bot: AsyncTeleBot, client: AsyncApiClient) -> None:
        self.bot = bot
        self._client = client

        self.bot.message_handler(commands=["start"])(self.start_handler)
        self.bot.message_handler(content_types=["text"])(self.task_handler)
        self.bot.callback_query_handler(func=lambda call: call.data != "registrate")(
            self.callback_handler
        )
        self.bot.callback_query_handler(func=lambda call: call.data == "registrate")(
            self.callback_registrate
        )

    async def start_handler(self, message: Message) -> None:
        keyboard = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="Регистрация", callback_data="registrate")
        keyboard.add(btn)
        await self.bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=keyboard)

    async def callback_registrate(self, call: CallbackQuery) -> None:
        try:
            await self._client.sign_up_user(call.message)
        except Exception as exc:
            logger.error(f"Problem when sign up user in API. {exc}")
            await self.bot.send_message(call.message.chat.id, ERROR_MESSAGE)
        else:
            await self.bot.send_message(call.message.chat.id, SUCCESS_SIGN_UP)

    @requires_auth
    async def task_handler(self, message: Message) -> None:
        logger.info("Starting to process user prompt...")
        await self.bot.send_message(message.chat.id, PROCESSING_MESSAGE)
        try:
            await self._client.create_task(message)
        except Exception as exc:
            logger.error(f"Problem when creating task in API. {exc}")
            await self.bot.send_message(message.chat.id, ERROR_MESSAGE)

        await self.bot.send_message(message.chat.id, "DONE", reply_markup=create_action_buttons())

    @requires_auth
    async def callback_handler(self, call: CallbackQuery) -> None:
        if call.data == CallbackData.ACCEPT:
            await self.bot.answer_callback_query(call.id, ACCEPTED_MESSAGE)
            await self.bot.send_message(
                call.message.chat.id, RATE_PROMPT_MESSAGE, reply_markup=create_rating_buttons()
            )

        elif call.data == CallbackData.REGENERATE:
            await self.bot.answer_callback_query(call.id, REGENERATING_MESSAGE)

        elif call.data.startswith("rate_"):
            await self._client.create_feedback(
                user_id=call.from_user.id,
                rating=int(call.data.split("_")[1]),
            )
            await self.bot.send_message(call.message.chat.id, RATE_THANKS_MESSAGE)
            await self.bot.send_message(call.message.chat.id, ASK_NEW_PROMPT_MESSAGE)
