from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from turbine.data_sources import S3TextDataSource
from turbine.vector_databases import MilvusVectorDB, PineconeVectorDB, SimilarityMetric
from turbine.embedding_models import HuggingFaceModel, OpenAIModel


VectorDatabase = MilvusVectorDB | PineconeVectorDB
EmbeddingModel = HuggingFaceModel | OpenAIModel
DataSource = S3TextDataSource


class PipelineSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_database: VectorDatabase
    embedding_model: EmbeddingModel
    data_source: DataSource

    def validate_config(self) -> None:
        self.data_source.validate_config()
        self.embedding_model.validate_config()
        self.vector_database.validate_config()


class PipelineSchemaGet(PipelineSchema):
    id: UUID
