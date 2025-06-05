from pathlib import Path

from ttk import DataType, Device, PythonModel, Shape, Venv

from models.main import Main
from settings import settings


_venv = Venv()
_venv.pip.install("numpy", "1.26.4")
_venv.pip.install("pillow", "10.2.0")
_venv.pip.install("torch", "2.4.1")
_venv.pip.install("diffusers", "0.30.3")
_venv.pip.install("peft", "0.12.0")
_venv.pip.install("transformers", "4.44.2")


main = PythonModel(
    group=settings.DEPLOYMENT_GROUP,
    name="main",
    version=settings.DEPLOYMENT_VERSION,
    input=Shape(dimensions=[-1], datatype=DataType.TYPE_UINT8),
    output=Shape(dimensions=[-1], datatype=DataType.TYPE_UINT8),
    model=Main(),
    venv=_venv,
    device=Device("gpu").instances(settings.MODEL_INSTANCES, index=0),
    data=Path(__file__).parent.parent.parent / ".build/main/.data",
)
