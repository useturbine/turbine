from abc import abstractmethod
from typing import LiteralString


class EmbeddingModel:
    type: LiteralString
    batch_size: int

    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        ...
