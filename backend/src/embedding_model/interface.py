from abc import abstractmethod
from typing import List


class EmbeddingModel:
    name: str
    embedding_dimension: int

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a given text."""
        pass
