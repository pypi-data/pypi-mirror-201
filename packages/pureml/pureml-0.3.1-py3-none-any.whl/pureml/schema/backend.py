from pydantic import BaseModel, root_validator
from .singleton import Singleton_BaseModel
import typing
import os


class BackendSchema(Singleton_BaseModel):

    BASE_URL: str = "https://pureml-development.up.railway.app/api/"
    FRONTEND_BASE_URL: str = "https://pureml.com/"
    INTEGRATIONS: dict = {
        "s3": {
            "name": "AWS S3 Object Storage",
            "secrets": [
                "access_key_id",
                "access_key_secret",
                "bucket_location",
                "bucket_name",
            ],
        },
        "r2": {
            "name": "Cloudflare R2 Object Storage",
            "secrets": [
                "access_key_id",
                "access_key_secret",
                "account_id",
                "bucket_name",
                "public_url",
            ],
        }
    }

    class Config:
        arbitrary_types_allowed = True
