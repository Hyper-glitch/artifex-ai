from pathlib import Path
from typing import Any

import torch
from diffusers import StableDiffusionXLPipeline


class Pipeline(StableDiffusionXLPipeline):
    @classmethod
    def build(
        cls, checkpoint: Path, device: torch.device, adapter: str | None = None, **kwargs: Any
    ) -> "Pipeline":
        """Builds a new pipeline instance"""
        pipeline: Pipeline = cls.from_pretrained(
            str(checkpoint),
            torch_dtype=torch.bfloat16,
            local_files_only=True,
            **kwargs,
        )

        if adapter:
            adapter_name = "current"
            pipeline.load_lora_weights(str(checkpoint / adapter), adapter_name=adapter_name)
            pipeline.set_adapters(adapter_name)

        pipeline.to(device)
        pipeline._current_device = device

        return pipeline
