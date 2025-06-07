import asyncio
import sys

from aiohttp import ClientError

from client import AsyncApiClient
from handler import Handlers
from loguru import logger
from settings import settings
from telebot.async_telebot import AsyncTeleBot


def prepare_logger() -> None:
    logger.remove()
    logger.add(sys.stderr, level=settings.LOG_LEVEL)
    logger.info("Logger initialized")


async def start_bot(bot: AsyncTeleBot) -> None:
    while True:
        try:
            logger.info("Starting bot polling...")
            await bot.infinity_polling(timeout=10, request_timeout=60)
        except (ClientError, asyncio.TimeoutError, OSError) as e:
            logger.error(f"Polling error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception:
            logger.exception("Unexpected exception in polling loop")
            await asyncio.sleep(5)


async def main() -> None:
    prepare_logger()

    bot = AsyncTeleBot(settings.TELEGRAM_BOT_TOKEN)
    client = AsyncApiClient(base_url=settings.API_CLIENT_URL, token=settings.API_CLIENT_AUTH_TOKEN)

    Handlers(bot=bot, client=client)

    logger.info("Bot is starting to work...")
    await start_bot(bot)
    logger.info("Bot has finished work.")


if __name__ == "__main__":
    asyncio.run(main())
