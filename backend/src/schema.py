from pydantic import BaseModel
from enum import Enum


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


class SimilarityMetric(Enum):
    Cosine = "cosine"
    Euclidean = "euclidean"
