import asyncio
from urllib.parse import urljoin

from aiohttp import ClientSession

from dto import TritonInput
from settings import settings


class AsyncTritonClient:
    def __init__(self, base_url: str, model_name: str) -> None:
        self._url = urljoin(base_url, f"/v2/models/{model_name}/infer")
        self._session = ClientSession()
        self._semaphore = asyncio.Semaphore(settings.TRITON_MAX_CONCURRENCY)

    async def infer(self, inputs: TritonInput) -> bytes:
        """
        Отправляет запрос на Triton и возвращает результат.

        inputs: структура данных для Triton API, например:
        {
          "inputs": [
            {
              "name": "prompt",
              "shape": [1],
              "datatype": "BYTES",
              "data": [...]
            }
          ]
        }
        """
        async with self._semaphore:
            async with self._session.post(self._url, json=inputs) as response:
                response.raise_for_status()
                raw_data = await response.json()

        return raw_data["outputs"][0]["data"]

    async def close(self) -> None:
        await self._session.close()
