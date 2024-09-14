import os
from fastapi import status

ENV: str = os.getenv("ENV")
if ENV not in ("dev", "stg", "prod", "local"):
    raise Exception(
        {"message": "Application environment not found"},
        status.HTTP_503_SERVICE_UNAVAILABLE,
    )

PORT = os.getenv("PORT", default=8000)
VERSION = os.getenv("VERSION", default="0.0.1")
DEBUG: bool = os.getenv("DEBUG", default=False)
PROJECT_NAME: str = os.getenv("PROJECT_NAME", default="task-orbit")
ALLOWED_HOSTS: str = os.getenv(
    "ALLOWED_HOSTS",
    default="",
)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "")
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
