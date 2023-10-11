from pydantic import BaseModel
from typing import Literal, Optional, List, Union
from turbine.vector_db import MilvusVectorDB, PineconeVectorDB
from turbine.embedding_model import HuggingFaceModel, OpenAIModel
from turbine.vector_db.types import SimilarityMetric


class DataSourceBase(BaseModel):
    fields: Optional[List[str]] = None
    filter: Optional[str] = None


class PostgresConfig(BaseModel):
    url: str
    table: str


class PostgresDataSource(DataSourceBase):
    type: Literal["postgres"]
    config: PostgresConfig


class MongoConfig(BaseModel):
    url: str
    collection: str


class MongoDataSource(DataSourceBase):
    type: Literal["mongo"]
    config: MongoConfig


DataSource = Union[PostgresDataSource, MongoDataSource]


EmbeddingModelName = Literal["text-embedding-ada-002", "all-MiniLM-L6-v2"]


class Project(BaseModel):
    data_source: DataSource
    embedding_model: EmbeddingModelName
    vector_db: Literal["milvus", "pinecone"]


class MilvusConfig(BaseModel):
    url: str
    token: str


class PineconeConfig(BaseModel):
    api_key: str
    environment: str


class PineconeSchema(BaseModel):
    type: Literal["pinecone"]
    config: PineconeConfig

    def get_instance(self):
        return PineconeVectorDB(
            api_key=self.config.api_key,
            environment=self.config.environment,
        )


class MilvusSchema(BaseModel):
    type: Literal["milvus"]
    config: MilvusConfig

    def get_instance(self):
        return MilvusVectorDB(
            url=self.config.url,
            token=self.config.token,
        )


VectorDBSchema = Union[MilvusSchema, PineconeSchema]


class HuggingFaceConfig(BaseModel):
    token: str
    model: str


class OpenAIConfig(BaseModel):
    api_key: str
    model: str


class HuggingFaceSchema(BaseModel):
    type: Literal["huggingface"]
    config: HuggingFaceConfig

    def get_instance(self):
        return HuggingFaceModel(
            token=self.config.token,
            model=self.config.model,
        )


class OpenAISchema(BaseModel):
    type: Literal["openai"]
    config: OpenAIConfig

    def get_instance(self):
        return OpenAIModel(
            api_key=self.config.api_key,
            model=self.config.model,
        )


EmbeddingModelSchema = Union[HuggingFaceSchema, OpenAISchema]


class IndexSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_db: VectorDBSchema
    embedding_model: EmbeddingModelSchema
    embedding_dimension: int
    similarity_metric: SimilarityMetric


class ExistingIndexSchema(IndexSchema):
    id: str
