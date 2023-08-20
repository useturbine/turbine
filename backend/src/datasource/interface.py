from abc import abstractmethod
from typing import Iterator, Tuple, Optional, TypedDict
from datetime import datetime


class DataSourceUpdate(TypedDict):
    data_source: str
    document_id: str
    document: Optional[str]


class DataSource:
    @abstractmethod
    def get_documents(
        self, updated_since: Optional[datetime] = None
    ) -> Iterator[Tuple[str, str]]:
        """Retrieve documents from the data source."""
        pass

    @abstractmethod
    def listen_for_updates(self) -> DataSourceUpdate:
        """Listen for updates to the data source and yield documents as they come in."""
        pass
