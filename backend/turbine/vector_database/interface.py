from typing import List
from abc import abstractmethod
from pydantic import BaseModel
from typing import Any


class VectorItem(BaseModel):
    id: str
    vector: List[float]
    metadata: dict[str, Any]


class VectorSearchResult(BaseModel):
    id: str
    score: float
    metadata: dict[str, Any]


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
