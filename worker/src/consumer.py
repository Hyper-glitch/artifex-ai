import logging

import aio_pika

from dto import RMQMessage
from service import GenAIProcessingService
from settings import settings


class RMQConsumer:
    """Асинхронный обработчик сообщений из RabbitMQ."""

    def __init__(self, gen_service: GenAIProcessingService):
        self._gen_service = gen_service

    async def consume(self) -> None:
        """Запускает потребителя сообщений."""
        connection = await aio_pika.connect_robust(settings.rmq_url)
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_NAME, durable=True)
        logging.info(f"The queue {settings.RABBITMQ_QUEUE_NAME} successfully declared.")

        async for message in queue:  # type: ignore[attr-defined]
            logging.info(f"Message received: {message.body}")
            await self._process_message(message)

    async def _process_message(self, message: aio_pika.IncomingMessage) -> None:
        """Обрабатывает одно сообщение из очереди."""
        async with message.process():
            try:
                msg = RMQMessage.model_validate_json(message.body)
                await self._gen_service.process_task(msg)
            except Exception as e:
                logging.error(f"Message processing error: {e}")
