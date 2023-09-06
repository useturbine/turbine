from pydantic import BaseModel
from typing import Literal


class PostgresConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str
    table: str


class MongoConfig(BaseModel):
    url: str
    collection: str


class PostgresDataSource(BaseModel):
    type: Literal["postgres"]
    config: PostgresConfig


class MongoDataSource(BaseModel):
    type: Literal["mongo"]
    config: MongoConfig


SimilarityMetric = Literal["cosine", "euclidean"]


class Project(BaseModel):
    data_source: PostgresDataSource | MongoDataSource
    embedding_model: Literal["openai"]
    vector_db: Literal["milvus", "pinecone"]
    similarity_metric: SimilarityMetric
