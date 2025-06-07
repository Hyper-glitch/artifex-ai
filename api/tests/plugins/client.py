import pytest
from httpx import ASGITransport, AsyncClient

from api.services.task import TaskService
from api.services.user import UserService


@pytest.fixture()
async def async_client(user_service: UserService, task_service: TaskService) -> AsyncClient:
    """Async client for testing application endpoints."""

    from api.dependepcies import (
        get_user_service,
        get_task_service
    )
    from api.main import app

    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[get_task_service] = lambda: task_service

    headers = {
        "Authorization": "TEST",
        "Content-Type": "application/json",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/api/v1", headers=headers,
    ) as client:
        yield client
