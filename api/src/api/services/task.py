import logging
from typing import Callable

from api.dto.rmq import RMQMessage
from api.dto.task import AITaskRequest, UpdateTaskRequest
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import TaskNotFoundException
from api.repositories.task import TaskRepository
from api.rmq import AsyncRabbitMQProducer
from settings import settings


class TaskService:
    def __init__(self, repo_factory: Callable[[AsyncSession], TaskRepository], producer: AsyncRabbitMQProducer) -> None:
        self._repo_factory = repo_factory
        self._producer = producer

    async def create(self, task_data: AITaskRequest, session: AsyncSession) -> None:
        """Создает и сохраняет новую AI задачу в БД и пушит в RMQ (транзакционно)."""
        try:
            async with session.begin():
                repo = self._repo_factory(session)
                task = await repo.create(task_data)
                await self._producer.publish(
                    queue_name=settings.RABBITMQ_QUEUE_NAME,
                    message=RMQMessage(
                        task_id=task.id,
                        prompt=task.prompt,
                        chat_id=task_data.chat_id,
                    ),
                )
        except Exception as exc:
            logging.error(f"Ошибка при создании задачи: {exc}", exc_info=True)
            raise

        logging.info(f"AITask - {task.id} - successfully created and published.")

    async def update(self, request: UpdateTaskRequest, session: AsyncSession) -> None:
        """Получает и обновляет задачу по ID."""
        repo = self._repo_factory(session)
        task = await repo.get(request.task_id)
        if not task:
            raise TaskNotFoundException()

        await repo.update(task, request.status)
        logging.info(f"AITask - {task.id} - status updated successfully.")
