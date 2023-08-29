from src.vectordb.interface import VectorDB, VectorItem, VectorSearchResult
import pinecone
from pinecone import Vector
from typing import List


class PineconeVectorDB(VectorDB):
    def __init__(self, api_key: str, environment: str) -> None:
        pinecone.init(api_key=api_key, environment=environment)

    @staticmethod
    def create_collection(name: str, dimension: int) -> None:
        pinecone.create_index(name, dimension=dimension)

    @staticmethod
    def insert(collection_name: str, data: List[VectorItem]) -> None:
        index = pinecone.Index(collection_name)
        index.upsert(
            vectors=[
                Vector(
                    values=vector["vector"],
                    id=vector["id"],
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
            {
                "id": result.id,
                "distance": result.score,
            }
            for result in results["matches"]
        ]

    @staticmethod
    def delete(collection_name: str, id: str) -> None:
        index = pinecone.Index(collection_name)
        index.delete(ids=[id])

    @staticmethod
    def drop_collection(collection_name: str) -> None:
        pinecone.delete_index(collection_name)
