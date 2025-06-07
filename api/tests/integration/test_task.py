import pytest
from fastapi import status
from httpx import AsyncClient

from api.dto.task import AITaskRequest, UpdateTaskRequest


class TestMLTaskService:
    _create_url = "tasks/create/"
    _update_url = "tasks/update/"

    @pytest.mark.asyncio
    async def test_create_task_success(self, async_client: AsyncClient, new_task_dto: AITaskRequest) -> None:
        """Тест успешного создания новой задачи на генерацию."""
        response = await async_client.post(
            self._create_url, json=new_task_dto.model_dump(mode="json")
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": True}

    @pytest.mark.asyncio
    async def test_update_task_success(self, async_client, update_task_request: UpdateTaskRequest) -> None:
        """Тест на успешное обновление задачи."""
        response = await async_client.post(
            self._update_url, json=update_task_request.model_dump()
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": True}

    @pytest.mark.asyncio
    async def test_update_task_failed(self, async_client, update_task_no_exists_request: UpdateTaskRequest) -> None:
        """Тест на неуспешное обновление задачи."""
        response = await async_client.post(
            self._update_url, json=update_task_no_exists_request.model_dump()
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"success": False, 'message': 'ML Task not found!'}
