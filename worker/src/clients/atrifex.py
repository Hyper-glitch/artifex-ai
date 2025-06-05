from urllib.parse import urljoin

from aiohttp import ClientSession

from enums import TaskStatus


class AsyncApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._session = self._create_session(token, base_url)

    async def update_task(self, task_id: str, status: TaskStatus, detail: str) -> None:
        async with self._session.post(
            "/worker/tasks/update/",
            json={"task_id": str(task_id), "status": status, "detail": detail},
        ) as resp:
            resp.raise_for_status()

    @staticmethod
    def _create_session(token: str, base_url: str) -> ClientSession:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        return ClientSession(headers=headers, base_url=urljoin(base_url, "/api/v1/"))
