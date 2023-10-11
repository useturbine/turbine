from abc import abstractmethod
from typing import Iterator, Tuple, Optional
from pydantic import BaseModel
from datetime import datetime


class DataSourceUpdate(BaseModel):
    project_id: str
    document_id: str
    document: Optional[str]


class DataSource:
    @abstractmethod
    def get_documents(self, **kwargs) -> Iterator[Tuple[str, str]]:
        """Retrieve all documents from the data source."""
        pass

    @abstractmethod
    def listen_for_updates(self, **kwargs) -> Iterator[DataSourceUpdate]:
        """Listen for updates to the data source and yield documents as they come in."""
        pass
