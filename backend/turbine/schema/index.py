from turbine.vector_db import MilvusVectorDB, PineconeVectorDB
from turbine.embedding_model import HuggingFaceModel, OpenAIModel
from pydantic import BaseModel
from typing import Optional
from turbine.vector_db.types import SimilarityMetric
from uuid import UUID


VectorDB = MilvusVectorDB | PineconeVectorDB
EmbeddingModelSchema = HuggingFaceModel | OpenAIModel


class IndexSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_db: VectorDB
    embedding_model: EmbeddingModelSchema
    embedding_dimension: int
    similarity_metric: SimilarityMetric


class ExistingIndexSchema(IndexSchema):
    id: UUID
