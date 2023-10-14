from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from turbine.data_source import S3TextDataSource
from turbine.vector_database import MilvusVectorDB, PineconeVectorDB, SimilarityMetric
from turbine.embedding_model import HuggingFaceModel, OpenAIModel


VectorDatabase = MilvusVectorDB | PineconeVectorDB
EmbeddingModel = HuggingFaceModel | OpenAIModel
DataSource = S3TextDataSource


class PipelineSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_database: VectorDatabase
    embedding_model: EmbeddingModel
    embedding_dimension: int
    similarity_metric: SimilarityMetric
    data_source: DataSource


class ExistingPipelineSchema(PipelineSchema):
    id: UUID
