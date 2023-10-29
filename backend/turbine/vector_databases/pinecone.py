from turbine.vector_databases import VectorDatabase, VectorItem, VectorSearchResult
import pinecone
from pinecone import Vector
from pydantic import BaseModel
from typing import Literal
from urllib3.exceptions import MaxRetryError


class PineconeVectorDB(VectorDatabase, BaseModel):
    type: Literal["pinecone"] = "pinecone"
    api_key: str
    environment: str
    index_name: str
    batch_size: int = 128

    def __init__(self, **data) -> None:
        super().__init__(**data)
        pinecone.init(api_key=self.api_key, environment=self.environment)

    def validate_config(self) -> None:
        try:
            pinecone.list_indexes()
        except pinecone.PineconeException:
            raise ValueError("Invalid Pinecone API key")
        except MaxRetryError:
            raise ValueError("Invalid Pinecone environment")
        try:
            pinecone.describe_index(self.index_name)
        except pinecone.PineconeException:
            raise ValueError("Invalid Pinecone index name")

    def insert(self, data: list[VectorItem]) -> None:
        index = pinecone.Index(self.index_name)
        index.upsert(
            vectors=[
                Vector(
                    id=vector.id,
                    values=vector.embedding,
                    metadata=vector.metadata,
                )
                for vector in data
            ]
        )

    def search(self, data: list[float], limit: int) -> list[VectorSearchResult]:
        index = pinecone.Index(self.index_name)
        results = index.query(vector=data, top_k=limit, include_metadata=True)
        return [
            VectorSearchResult(
                id=result.id, score=result.score, metadata=result.metadata
            )
            for result in results["matches"]
        ]

    def delete(self, id: str) -> None:
        index = pinecone.Index(self.index_name)
        index.delete(ids=[id])
