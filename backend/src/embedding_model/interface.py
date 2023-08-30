from abc import abstractmethod
from typing import List
from enum import Enum


class DistanceFunction(Enum):
    Cosine = "cosine"
    Euclidean = "euclidean"


class EmbeddingModel:
    embedding_dimension: int
    distance_function: DistanceFunction

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a given text."""
        pass
