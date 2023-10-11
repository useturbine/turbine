from turbine.vector_db.interface import VectorDB, VectorItem, VectorSearchResult
import pinecone
from pinecone import Vector
from typing import List
from .types import SimilarityMetric
from uuid import UUID


class PineconeVectorDB(VectorDB):
    @staticmethod
    def get_collection_name(index_id: UUID) -> str:
        return f"turbine-{index_id}"

    def __init__(self, api_key: str, environment: str) -> None:
        pinecone.init(api_key=api_key, environment=environment)

    @staticmethod
    def create_collection(
        name: str, dimension: int, similarity_metric: SimilarityMetric
    ) -> None:
        pinecone.create_index(name, dimension=dimension, metric=similarity_metric)

    @staticmethod
    def insert(collection_name: str, data: List[VectorItem]) -> None:
        index = pinecone.Index(collection_name)
        index.upsert(
            vectors=[
                Vector(
                    values=vector.vector,
                    id=vector.id,
                )
                for vector in data
            ]
        )

    @staticmethod
    def search(
        collection_name: str, data: List[float], limit: int
    ) -> List[VectorSearchResult]:
        index = pinecone.Index(collection_name)
        results = index.query(
            vector=data,
            top_k=limit,
        )
        return [
            VectorSearchResult(id=result.id, score=result.score)
            for result in results["matches"]
        ]

    @staticmethod
    def delete(collection_name: str, id: str) -> None:
        index = pinecone.Index(collection_name)
        index.delete(ids=[id])

    @staticmethod
    def drop_collection(collection_name: str) -> None:
        pinecone.delete_index(collection_name)
