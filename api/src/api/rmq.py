import logging

import aio_pika
from aio_pika import Connection
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue
from settings import settings

from api.dto.rmq import RMQMessage


class AsyncRabbitMQProducer:
    """Асинхронный клиент для RabbitMQ."""

    _channel: AbstractChannel | None = None
    _exchange: AbstractExchange
    _queue: AbstractQueue

    def __init__(self) -> None:
        self._connection: Connection | None = None

    async def connect(self) -> None:
        """Подключение к RabbitMQ и инициализация exchange и queue."""
        logging.info("Connecting to RabbitMQ...")

        connection = await aio_pika.connect_robust(settings.rmq_url)
        self._channel = await connection.channel()
        self._exchange = await self._channel.declare_exchange(
            aio_pika.ExchangeType.DIRECT.value, aio_pika.ExchangeType.DIRECT
        )
        self._queue = await self._channel.declare_queue(settings.RABBITMQ_QUEUE_NAME, durable=True)
        await self._queue.bind(self._exchange)

        logging.info(
            f"The queue {settings.RABBITMQ_QUEUE_NAME} "
            f"tied to exchange {aio_pika.ExchangeType.DIRECT.value}"
        )

    async def publish(self, queue_name: str, message: RMQMessage) -> None:
        """Публикует сообщение в очередь."""
        if not self._channel:
            logging.info("The RMQ channel is not set....")
            await self.connect()

        await self._exchange.publish(
            aio_pika.Message(
                body=message.model_dump_json().encode("utf-8"),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self._queue.name,
        )
        logging.info(f"Message successfully sent to the queue {queue_name}")

    async def close(self) -> None:
        """Закрывает соединение с RabbitMQ."""
        if self._connection:
            await self._connection.close()
