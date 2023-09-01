from pydantic import BaseModel
from typing import Literal
from src.schema import PostgresConfig, MongoConfig


class PostgresDataSource(BaseModel):
    type: Literal["postgres"]
    config: PostgresConfig


class MongoDataSource(BaseModel):
    type: Literal["mongo"]
    config: MongoConfig


class Project(BaseModel):
    data_source: PostgresDataSource | MongoDataSource
    embedding_model: Literal["openai"]
    vector_db: Literal["milvus"]
    similarity_metric: Literal["cosine"]
