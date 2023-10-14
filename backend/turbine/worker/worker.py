from celery import Celery, group
from celery.app.task import Context
from config import Config
from turbine.database import Pipeline, Task
from turbine.schema import ExistingPipelineSchema
from turbine.data_source import DataSourceDocument
from turbine.vector_database import VectorItem
from datetime import datetime
from uuid import UUID
from types import TracebackType
from logging import getLogger


app = Celery(
    "turbine", backend=Config.celery_backend_url, broker=Config.celery_broker_url
)
logger = getLogger(__name__)


@app.task
def run_pipeline(pipeline_id: str, task_id: str):
    pipeline: ExistingPipelineSchema = Pipeline.get_by_id(pipeline_id).dump()
    documents = [
        document.model_dump() for document in pipeline.data_source.get_documents()
    ]
    chains = group(
        (
            create_embedding.s(pipeline_id, document)
            | store_embedding.s(pipeline_id, document["id"])
        )
        for document in documents
    ) | on_task_success.si(task_id).on_error(on_task_error.s(task_id))
    chains.delay()


@app.task
def create_embedding(pipeline_id: str, document: dict):
    document_parsed = DataSourceDocument(**document)
    pipeline: ExistingPipelineSchema = Pipeline.get_by_id(pipeline_id).dump()
    embedding = pipeline.embedding_model.get_embedding(document_parsed.text)
    return embedding


@app.task
def store_embedding(
    embedding: list[float],
    pipeline_id: str,
    document_id: str,
):
    pipeline: ExistingPipelineSchema = Pipeline.get_by_id(pipeline_id).dump()
    pipeline.vector_database.insert([VectorItem(id=document_id, vector=embedding)])


@app.task
def on_task_success(task_id: str, *args):
    try:
        task = Task.get_by_id(task_id)
        task.finished_at = datetime.now()
        task.successful = True
        task.save()
    except Exception as e:
        logger.error("Error while saving task details after task success", e)


@app.task
def on_task_error(
    context: Context, error: Exception, traceback: TracebackType, task_id: UUID, *args
):
    try:
        task = Task.get_by_id(task_id)
        task.finished_at = datetime.now()
        task.successful = False
        task.save()
    except Exception as e:
        logger.error("Error while saving task details after task error", e)
