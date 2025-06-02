from datetime import datetime

from api.dto.task import AITaskRequest
from enums import TaskStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.task import AITask


class TaskRepository:
    """Репозиторий для управления задачами."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, task_dto: AITaskRequest) -> AITask:
        """Создает и сохраняет новую AI задачу в БД."""
        task = AITask(
            id=task_dto.task_id,
            user_id=task_dto.user_id,
            prompt=task_dto.prompt,
            status=task_dto.status,
            created_at=task_dto.created_at,
        )
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)

        return task

    async def update(self, task: AITask, status: TaskStatus) -> None:
        """Обновляет статус задачи и сохраняет результат."""
        task = await self.get(task.id)
        task.status = status
        task.completed_at = (
            datetime.utcnow() if status != TaskStatus.PROCESSING else None
        )
        await self._session.commit()

    async def get(self, task_id: str) -> AITask | None:
        """Получает задачу по ID."""
        result = await self._session.execute(select(AITask).filter_by(id=task_id))
        task = result.scalars().one_or_none()
        return task
