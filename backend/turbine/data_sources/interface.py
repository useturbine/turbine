from abc import abstractmethod
from pydantic import BaseModel
from turbine.types import Document


class DataSource(BaseModel):
    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def get_keys(self) -> list[str]:
        ...

    @abstractmethod
    def get_documents(self, key: str) -> list[Document]:
        ...
