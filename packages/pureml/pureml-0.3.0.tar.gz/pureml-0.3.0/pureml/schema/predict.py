from pydantic import BaseModel
from .backend import BackendSchema
from .paths import PathSchema
import os
from .types import DataTypes


class Input(BaseModel):
    type: DataTypes
    shape: tuple = None


class Output(BaseModel):
    type: DataTypes = None
    shape: tuple = None


class PredictSchema(BaseModel):
    paths: PathSchema = PathSchema().get_instance()
    backend: BackendSchema = BackendSchema().get_instance()

    PATH_PREDICT_REQUIREMENTS: str = os.path.join(
        paths.PATH_PREDICT_DIR, "requirements.txt"
    )
    PATH_PREDICT: str = os.path.join(paths.PATH_PREDICT_DIR, "predict.py")

    PATH_PREDICT_USER: str = os.path.join(os.getcwd(), "predict.py")
    PATH_PREDICT_REQUIREMENTS_USER: str = os.path.join(os.getcwd(), "requirements.txt")
    PATH_RESOURCES: str = os.path.join(paths.PATH_PREDICT_DIR, "resources.zip")
    PATH_RESOURCES_DIR_DEFAULT: str = os.getcwd()
    resource_format: str = "zip"

    folders_to_ignore: list = ["./.pureml", "./.venv"]

    class Config:
        arbitrary_types_allowed = True
