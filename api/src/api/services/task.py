import logging
from typing import Callable

from api.dto.task import AITaskRequest, UpdateTaskRequest
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import TaskNotFoundException
from api.repositories.task import TaskRepository
from models.task import AITask


class TaskService:
    def __init__(self, repo_factory: Callable[[AsyncSession], TaskRepository]) -> None:
        self._repo_factory = repo_factory

    async def create(self, task_data: AITaskRequest, session: AsyncSession) -> AITask:
        """Создает и сохраняет новую AI задачу в БД."""
        repo = self._repo_factory(session)
        task = await repo.create(task_data)
        logging.info(f"AITask - {task.id} - created successfully.")

        return task

    async def update(self, request: UpdateTaskRequest, session: AsyncSession) -> None:
        """Получает и обновляет задачу по ID."""
        repo = self._repo_factory(session)
        task = await repo.get(request.task_id)
        if not task:
            raise TaskNotFoundException()

        await repo.update(task, request.status)
        logging.info(f"AITask - {task.id} - status updated successfully.")
