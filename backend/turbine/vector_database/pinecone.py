from turbine.vector_database import VectorDB, VectorItem, VectorSearchResult
import pinecone
from pinecone import Vector
from typing import List
from pydantic import BaseModel
from typing import Literal


class PineconeVectorDB(VectorDB, BaseModel):
    type: Literal["pinecone"]
    api_key: str
    environment: str
    index_name: str

    def __init__(self, **data) -> None:
        super().__init__(**data)
        pinecone.init(api_key=self.api_key, environment=self.environment)

    def insert(self, data: List[VectorItem]) -> None:
        index = pinecone.Index(self.index_name)
        index.upsert(
            vectors=[
                Vector(
                    id=vector.id,
                    values=vector.vector,
                    metadata=vector.metadata,
                )
                for vector in data
            ]
        )

    def search(self, data: List[float], limit: int) -> List[VectorSearchResult]:
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
