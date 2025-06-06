"""Module to perform inference requests

Requests are sent to Triton inference server.
Requests are sent to the main entrypoint deployed with `deployment.py` script.
"""

import click
import numpy as np
from PIL import Image
from ttk import ProxyModel

from deployment import main
from settings import settings


@click.command()
@click.option("--prompt", help="user input for generate content", type=str, required=False)
def request(prompt: str | None = None) -> None:
    """Prepare input data and send it to the Triton Server."""
    np_prompt = np.array([prompt], dtype=np.object_)
    model = ProxyModel.from_model(model=main, url=settings.TRITON_CLIENT_URL)

    response = model.request(inputs=[np_prompt])
    gen_image = Image.fromarray(response[0])
    gen_image.show()


if __name__ == "__main__":
    request()
