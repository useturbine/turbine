from typing import List
from abc import abstractmethod
from pydantic import BaseModel


class VectorItem(BaseModel):
    id: str
    vector: List[float]


class VectorSearchResult(BaseModel):
    id: str
    score: float


class VectorDB:
    @abstractmethod
    def insert(self, data: List[VectorItem]) -> None:
        ...

    @abstractmethod
    def search(self, data: List[float], limit: int) -> List[VectorSearchResult]:
        ...

    @abstractmethod
    def delete(self, id: str) -> None:
        ...
