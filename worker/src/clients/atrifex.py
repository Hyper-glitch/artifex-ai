from urllib.parse import urljoin

from aiohttp import ClientSession

from dto import UpdateTaskRequest


class AsyncApiClient:
    def __init__(self, base_url: str, token: str) -> None:
        self._session = self._create_session(token, base_url)

    async def update_task(self, dto: UpdateTaskRequest) -> None:
        async with self._session.post("tasks/update/", json=dto.model_dump()) as resp:
            resp.raise_for_status()

    @staticmethod
    def _create_session(token: str, base_url: str) -> ClientSession:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        return ClientSession(headers=headers, base_url=urljoin(base_url, "/api/v1/"))
