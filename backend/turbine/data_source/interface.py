from abc import abstractmethod
from pydantic import BaseModel
from typing import Any


class DataSourceDocument(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any]


class DataSource:
    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def get_keys(self) -> list[str]:
        ...

    @abstractmethod
    def get_documents(self, key: str) -> list[DataSourceDocument]:
        ...
