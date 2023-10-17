from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    postgres_url: str
    celery_broker_url: str
    celery_backend_url: str
    aws_access_key_id: str
    aws_secret_access_key: str


config = Config(
    postgres_url=os.getenv("POSTGRES_URL"),
    celery_broker_url=os.getenv("CELERY_BROKER_URL"),
    celery_backend_url=os.getenv("CELERY_BACKEND_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
