import uuid
from datetime import datetime

import pytest
from faker import Faker

from api.dto.task import UpdateTaskRequest, AITaskRequest
from api.services.task import TaskService
from enums import TaskStatus
from models import AITask

fake = Faker()


@pytest.fixture()
def new_task_dto() -> AITaskRequest:
    return AITaskRequest(
        user_id=1,
        task_id=str(uuid.uuid4()),
        prompt=fake.text(max_nb_chars=100),
        status=TaskStatus.NEW,
        chat_id=1,
        created_at=datetime.utcnow()
    )


@pytest.fixture()
async def created_task(task_service: TaskService, new_task_dto: AITaskRequest, async_session) -> AITask:
    return await task_service.create(new_task_dto, async_session)


@pytest.fixture()
async def update_task_request(created_task: AITask) -> UpdateTaskRequest:
    return UpdateTaskRequest(
        task_id=created_task.id,
        rating=5,
        status=TaskStatus.COMPLETED,
        logs="inference completed",
    )


@pytest.fixture()
async def update_task_no_exists_request() -> UpdateTaskRequest:
    return UpdateTaskRequest(
        task_id=str(uuid.uuid4()),
        rating=5,
        status=TaskStatus.COMPLETED,
        logs="inference completed",
    )
