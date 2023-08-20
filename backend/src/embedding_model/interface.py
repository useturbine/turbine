from abc import abstractmethod
from typing import List


class EmbeddingModel:
    encoding_base: str
    encoding_model: str
    embedding_dimension: int

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a given text."""
        pass
