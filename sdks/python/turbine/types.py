from typing import Literal
from pydantic import BaseModel


class PostgresConfig(BaseModel):
    host: str
    port: int
    database: str
    table: str
    user: str
    password: str


class MongoConfig(BaseModel):
    url: str
    collection: str


class DataSource(BaseModel):
    type: Literal["postgres", "mongo"]
    config: PostgresConfig or MongoConfig


class ProjectConfig(BaseModel):
    data_source: DataSource
    vector_db: Literal["milvus", "pinecone"]
    embedding_model: Literal["openai"]
    similarity_metric: Literal["cosine", "euclidean"]


class Project(BaseModel):
    id: str
    config: ProjectConfig


class SearchResult(BaseModel):
    id: str
    score: float
