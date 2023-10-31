from turbine.vector_databases import VectorDatabase, VectorDocument, VectorSearchResult
import pinecone
from pinecone import Vector
from typing import Literal
from urllib3.exceptions import MaxRetryError


class Pinecone(VectorDatabase):
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

    def insert(self, data: list[VectorDocument]) -> None:
        index = pinecone.Index(self.index_name)
        index.upsert(
            vectors=[
                Vector(
                    id=document.id,
                    values=document.embedding,
                    metadata=dict(**document.metadata, content=document.content),
                )
                for document in data
            ]
        )

    def search(self, data: list[float], limit: int) -> list[VectorSearchResult]:
        index = pinecone.Index(self.index_name)
        results = index.query(vector=data, top_k=limit, include_metadata=True)

        search_results: list[VectorSearchResult] = []
        for result in results["matches"]:
            metadata = result.metadata
            content = metadata.pop("content")
            search_results.append(
                VectorSearchResult(
                    id=result.id,
                    score=result.score,
                    metadata=metadata,
                    content=content,
                )
            )
        return search_results

    def delete(self, id: str) -> None:
        index = pinecone.Index(self.index_name)
        index.delete(ids=[id])

    @property
    def embedding_dimension(self) -> int:
        index = pinecone.describe_index(self.index_name)
        return index.dimension
