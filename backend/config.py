from dotenv import load_dotenv
import os
from pydantic import BaseModel


load_dotenv()


class Config(BaseModel):
    postgres_url: str
    # celery_broker_url: str
    # celery_backend_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    sentry_dsn: str


try:
    config = Config(
        postgres_url=os.environ["POSTGRES_URL"],
        # celery_broker_url=os.environ["CELERY_BROKER_URL"],
        # celery_backend_url=os.environ["CELERY_BACKEND_URL"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        sentry_dsn=os.environ["SENTRY_DSN"],
    )
except KeyError:
    raise ValueError("Missing required environment variable")
