from celery import Celery
from config import Config

app = Celery(
    "turbine", backend=Config.celery_backend_url, broker=Config.celery_broker_url
)


@app.task
def add(x, y):
    return x + y
