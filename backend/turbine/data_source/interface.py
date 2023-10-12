from abc import abstractmethod
from typing import Iterator, Tuple, Optional
from pydantic import BaseModel


class DataSourceUpdate(BaseModel):
    project_id: str
    document_id: str
    document: Optional[str]


class DataSource:
    @abstractmethod
    def get_documents(self) -> Iterator[Tuple[str, str]]:
        ...
