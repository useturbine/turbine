from typing import List
from abc import abstractmethod
from .types import SimilarityMetric
from pydantic import BaseModel
from uuid import UUID


class VectorItem(BaseModel):
    id: str
    vector: List[float]


class VectorSearchResult(BaseModel):
    id: str
    score: float


class VectorDB:
    @staticmethod
    @abstractmethod
    def get_collection_name(index_id: UUID) -> str:
        ...

    @abstractmethod
    def create_collection(
        self, name: str, dimension: int, similarity_metric: SimilarityMetric
    ) -> None:
        """Create a new collection in the database."""
        pass

    @abstractmethod
    def insert(self, collection_name: str, data: List[VectorItem]) -> None:
        """Insert data into the specified collection."""
        pass

    @abstractmethod
    def search(
        self, collection_name: str, data: List[float], limit: int
    ) -> List[VectorSearchResult]:
        """Search for vectors in the specified collection."""
        pass

    @abstractmethod
    def delete(self, collection_name: str, id: str) -> None:
        """Delete a specific entry from the collection."""
        pass

    @abstractmethod
    def drop_collection(self, collection_name: str) -> None:
        """Drop the specified collection from the database."""
        pass
