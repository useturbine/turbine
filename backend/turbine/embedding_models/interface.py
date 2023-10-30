from abc import abstractmethod
from typing import Optional
from pydantic import BaseModel


class EmbeddingModel(BaseModel):
    type: str
    batch_size: int
    _sample_embedding: Optional[list[float]] = None

    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        ...

    def get_sample_embedding(self) -> list[float]:
        return self.get_embeddings(["test"])[0]

    @property
    def embedding_dimension(self) -> int:
        if self._sample_embedding is None:
            self._sample_embedding = self.get_sample_embedding()
        return len(self._sample_embedding)
