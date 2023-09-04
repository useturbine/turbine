from abc import abstractmethod
from typing import List
from src.schema import SimilarityMetric


class EmbeddingModel:
    embedding_dimension: int
    similarity_metric: SimilarityMetric

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a given text."""
        pass
