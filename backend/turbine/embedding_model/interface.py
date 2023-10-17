from abc import abstractmethod
from typing import List


class EmbeddingModel:
    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        ...
