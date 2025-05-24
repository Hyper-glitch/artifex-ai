import asyncio
import sys

from client import AsyncApiClient
from handler import Handlers
from loguru import logger
from settings import settings
from telebot.async_telebot import AsyncTeleBot


def prepare_logger() -> None:
    logger.remove()
    logger.add(sys.stderr, level=settings.LOG_LEVEL)
    logger.info("Logger initialized")


async def main() -> None:
    prepare_logger()

    bot = AsyncTeleBot(settings.TELEGRAM_BOT_TOKEN)
    client = AsyncApiClient(base_url=settings.API_CLIENT_URL, token=settings.API_CLIENT_AUTH_TOKEN)

    Handlers(bot=bot, client=client)

    logger.info("Bot is starting to work...")
    await bot.polling(non_stop=True)
    logger.info("Bot has finished work.")


if __name__ == "__main__":
    asyncio.run(main())
