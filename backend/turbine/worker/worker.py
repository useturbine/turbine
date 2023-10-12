from celery import Celery
from config import Config
from uuid import UUID
from turbine.db.models import Pipeline

app = Celery(
    "turbine", backend=Config.celery_backend_url, broker=Config.celery_broker_url
)


@app.task
def run_pipeline(id: UUID):
    pipeline = Pipeline.get_or_none(Pipeline.id == id)
    if not pipeline:
        return

    print("Running pipeline", pipeline.id)
