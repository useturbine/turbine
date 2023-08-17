from abc import abstractmethod
from typing import List


class Model:
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a given text."""
        pass
