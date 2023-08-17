from abc import abstractmethod
from typing import Iterator, Tuple


class DataSource:
    @abstractmethod
    def get_all_documents(self) -> Iterator[Tuple[str, str]]:
        """Retrieve all documents from the data source."""
        pass

    @abstractmethod
    def get_new_documents(self) -> Iterator[Tuple[str, str]]:
        """Retrieve documents that were added/updated after the last fetched time."""
        pass
