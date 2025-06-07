import numpy as np
from ttk import PythonAbstractModel, Tensor

from .pipeline import Pipeline
from .preprocessor import Preprocessor


class Main(PythonAbstractModel):
    """Wrapper for python backend in Triton Inference Server."""

    _adapter: str = "pytorch_lora_weights_1000.safetensors"
    _height: int = 512
    _width: int = 512

    def _initialize(self) -> None:
        self._pipe = Pipeline.build(
            checkpoint=self.data, device=self.config.device, adapter=self._adapter
        )
        self._preproc = Preprocessor()

    def process(
        self, inputs: list[Tensor], parameters: dict[str, str | int | bool]
    ) -> list[Tensor]:
        prompt = self._preproc.preprocess(base_prompt=inputs[0].string)
        output = self._pipe(prompt, height=self._height, width=self._width).images[0]
        np_image = np.array(output)

        return [Tensor.from_numpy(np_image)]
