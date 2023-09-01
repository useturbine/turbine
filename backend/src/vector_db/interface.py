from typing import List, TypedDict
from abc import abstractmethod


class VectorItem(TypedDict):
    id: str
    vector: List[float]


class VectorSearchResult(TypedDict):
    id: str
    score: float


class VectorDB:
    """
    An interface defining the operations for interacting with a vector database.
    Classes that implement this interface must provide concrete implementations
    for all methods to interact with the database.

    Note:
        This is an interface and methods should be implemented in the derived classes.
    """

    @abstractmethod
    def create_collection(self, name: str, dimension: int) -> None:
        """Create a new collection in the database."""
        pass

    @abstractmethod
    def insert(self, collection_name: str, data: List[VectorItem]) -> None:
        """Insert data into the specified collection."""
        pass

    @abstractmethod
    def search(
        self, collection_name: str, data: List[float], limit: int
    ) -> List[VectorSearchResult]:
        """Search for vectors in the specified collection."""
        pass

    @abstractmethod
    def delete(self, collection_name: str, id: str) -> None:
        """Delete a specific entry from the collection."""
        pass

    @abstractmethod
    def drop_collection(self, collection_name: str) -> None:
        """Drop the specified collection from the database."""
        pass
