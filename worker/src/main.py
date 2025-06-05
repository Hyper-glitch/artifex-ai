import asyncio
import logging

from clients.atrifex import AsyncApiClient
from clients.tg_bot import TgBotClient
from clients.triton import AsyncTritonClient
from consumer import RMQConsumer
from logger import set_up_logger
from service import GenAIProcessingService
from settings import settings


async def main() -> None:
    """Запуск асинхронного воркера."""
    set_up_logger()

    api_cleint = AsyncApiClient(base_url=settings.BASE_API_URL, token=settings.API_AUTH_TOKEN)
    triton_client = AsyncTritonClient(base_url="", model_name=settings.TRITON_MODEL_NAME)
    tg_bot = TgBotClient(token=settings.TG_BOT_TOKEN)
    svc = GenAIProcessingService(
        api_cleint=api_cleint,
        triton_client=triton_client,
        tg_bot=tg_bot,
    )

    consumer = RMQConsumer(svc)
    logging.info("GenAI Worker started. Waiting for messages...")
    await consumer.consume()


if __name__ == "__main__":
    asyncio.run(main())
