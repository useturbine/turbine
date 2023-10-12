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


EmbeddingModelName = Literal["text-embedding-ada-002", "all-MiniLM-L6-v2"]


class Project(BaseModel):
    data_source: DataSource
    embedding_model: EmbeddingModelName
    vector_db: Literal["milvus", "pinecone"]
