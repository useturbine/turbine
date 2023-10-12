from turbine.vector_db import MilvusVectorDB, PineconeVectorDB
from turbine.embedding_model import HuggingFaceModel, OpenAIModel
from pydantic import BaseModel
from typing import Literal, Optional
from turbine.vector_db.types import SimilarityMetric


class MilvusConfig(BaseModel):
    url: str
    token: str

    def get_instance(self):
        return MilvusVectorDB(
            url=self.url,
            token=self.token,
        )


class PineconeConfig(BaseModel):
    api_key: str
    environment: str

    def get_instance(self):
        return PineconeVectorDB(
            api_key=self.api_key,
            environment=self.environment,
        )


class PineconeSchema(BaseModel):
    type: Literal["pinecone"]
    config: PineconeConfig


class MilvusSchema(BaseModel):
    type: Literal["milvus"]
    config: MilvusConfig


VectorDBSchema = MilvusSchema | PineconeSchema


class HuggingFaceConfig(BaseModel):
    token: str
    model: str

    def get_instance(self):
        return HuggingFaceModel(
            token=self.token,
            model=self.model,
        )


class OpenAIConfig(BaseModel):
    api_key: str
    model: str

    def get_instance(self):
        return OpenAIModel(
            api_key=self.api_key,
            model=self.model,
        )


class HuggingFaceSchema(BaseModel):
    type: Literal["huggingface"]
    config: HuggingFaceConfig


class OpenAISchema(BaseModel):
    type: Literal["openai"]
    config: OpenAIConfig


EmbeddingModelSchema = HuggingFaceSchema | OpenAISchema


class IndexSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_db: VectorDBSchema
    embedding_model: EmbeddingModelSchema
    embedding_dimension: int
    similarity_metric: SimilarityMetric


class ExistingIndexSchema(IndexSchema):
    id: str
