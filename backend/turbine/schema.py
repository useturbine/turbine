from pydantic import BaseModel
from typing import Literal, Optional, List, Union


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


SimilarityMetric = Literal["cosine", "euclidean"]
EmbeddingModel = Literal["text-embedding-ada-002", "all-MiniLM-L6-v2"]


class Project(BaseModel):
    data_source: DataSource
    embedding_model: EmbeddingModel
    vector_db: Literal["milvus", "pinecone"]


class MilvusConfig(BaseModel):
    url: str
    token: Optional[str] = None


class PineconeConfig(BaseModel):
    api_key: str
    environment: str


class PineconeVectorDB(BaseModel):
    type: Literal["pinecone"]
    config: PineconeConfig


class MilvusVectorDB(BaseModel):
    type: Literal["milvus"]
    config: MilvusConfig


class HuggingFaceConfig(BaseModel):
    token: str
    model: str


class OpenAIConfig(BaseModel):
    api_key: str
    model: str


class HuggingFaceModel(BaseModel):
    type: Literal["huggingface"]
    config: HuggingFaceConfig


class OpenAIModel(BaseModel):
    type: Literal["openai"]
    config: OpenAIConfig


class Index(BaseModel):
    name: str
    description: Optional[str] = None
    vector_db: Union[MilvusVectorDB, PineconeVectorDB]
    embedding_model: Union[HuggingFaceModel, OpenAIModel]
