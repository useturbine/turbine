from typing import List, Any
from pymilvus import Collection
from abc import abstractmethod


class VectorDBInterface:
    """
    An interface defining the operations for interacting with a vector database.
    Classes that implement this interface must provide concrete implementations
    for all methods to interact with the database.

    Note:
        This is an interface and methods should be implemented in the derived classes.
    """

    @staticmethod
    @abstractmethod
    def create_collection(name: str, id_max_length: int, dimension: int) -> Collection:
        """Create a new collection in the database."""
        pass

    @staticmethod
    @abstractmethod
    def insert(collection_name: str, data: List) -> None:
        """Insert data into the specified collection."""
        pass

    @staticmethod
    @abstractmethod
    def search(collection_name: str, data: List[float], limit: int) -> Any:
        """Search for vectors in the specified collection."""
        pass

    @staticmethod
    @abstractmethod
    def delete(collection_name: str, id: str) -> None:
        """Delete a specific entry from the collection."""
        pass

    @staticmethod
    @abstractmethod
    def drop_collection(collection_name: str) -> None:
        """Drop the specified collection from the database."""
        pass
