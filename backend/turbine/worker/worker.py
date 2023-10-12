from celery import Celery
from config import Config
from uuid import UUID
from turbine.db.models import Pipeline, Index
from turbine.schema import ExistingPipelineSchema, ExistingIndexSchema
from turbine.data_source import DataSourceDocument
from turbine.vector_db import VectorItem

app = Celery(
    "turbine", backend=Config.celery_backend_url, broker=Config.celery_broker_url
)


@app.task
def run_pipeline(pipeline_id: UUID):
    pipeline: ExistingPipelineSchema = Pipeline.get_by_id(pipeline_id).dump()
    documents = pipeline.data_source.get_documents()
    for document in documents:
        create_embedding.delay(pipeline_id, document.model_dump())


@app.task
def create_embedding(pipeline_id: UUID, document: dict):
    document_parsed = DataSourceDocument(**document)
    index: ExistingIndexSchema = (
        Index.select().join(Pipeline).where(Pipeline.id == pipeline_id).first().dump()
    )
    embedding = index.embedding_model.get_embedding(document_parsed.text)
    print(embedding)


# @app.task
# def store_embedding(pipeline_id: UUID, embedding: list[float]):
#     index: ExistingIndexSchema = (
#         Index.select().join(Pipeline).where(Pipeline.id == pipeline_id).first().dump()
#     )
#     collection_name = index.vector_db.get_collection_name(index.id)
#     index.vector_db.insert(
#         collection_name, [VectorItem(id=document_id, vector=embedding)]
#     )
