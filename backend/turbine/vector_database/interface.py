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
        ...

    @abstractmethod
    def insert(self, collection_name: str, data: List[VectorItem]) -> None:
        ...

    @abstractmethod
    def search(
        self, collection_name: str, data: List[float], limit: int
    ) -> List[VectorSearchResult]:
        ...

    @abstractmethod
    def delete(self, collection_name: str, id: str) -> None:
        ...

    @abstractmethod
    def drop_collection(self, collection_name: str) -> None:
        ...
