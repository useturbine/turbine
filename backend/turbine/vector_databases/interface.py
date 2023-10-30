from typing import List
from abc import abstractmethod
from pydantic import BaseModel
from typing import Any, LiteralString


class VectorItem(BaseModel):
    id: str
    embedding: List[float]
    metadata: dict[str, Any]


class VectorSearchResult(BaseModel):
    id: str
    score: float
    metadata: dict[str, Any]


class VectorDatabase:
    type: LiteralString
    batch_size: int

    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def insert(self, data: List[VectorItem]) -> None:
        ...

    @abstractmethod
    def search(self, data: List[float], limit: int) -> List[VectorSearchResult]:
        ...

    @abstractmethod
    def delete(self, id: str) -> None:
        ...

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        ...
