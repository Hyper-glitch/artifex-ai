import asyncio
from urllib.parse import urljoin

from aiohttp import ClientSession
import numpy as np

from dto import TritonInput, RMQMessage, Inputs
from settings import settings


class AsyncTritonClient:
    def __init__(self, base_url: str, model_name: str) -> None:
        self._url = urljoin(base_url, f"/v2/models/{model_name}/infer")
        self._session = ClientSession()
        self._semaphore = asyncio.Semaphore(settings.TRITON_MAX_CONCURRENCY)

    async def infer(self, msg: RMQMessage) -> np.ndarray:
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
        inputs = [Inputs(data=[msg.prompt])]
        data = TritonInput(inputs=inputs).model_dump()
        async with self._semaphore:
            async with self._session.post(self._url, json=data) as response:
                response.raise_for_status()
                raw_data = await response.json()

        int_list = raw_data["outputs"][0]["data"]
        return np.array(int_list, dtype=np.uint8).reshape((settings.GEN_IMAGE_WIDTH, settings.GEN_IMAGE_HEIGHT, 3))

    async def close(self) -> None:
        await self._session.close()
