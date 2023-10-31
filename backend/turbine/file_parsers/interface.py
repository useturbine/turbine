import magic
from typing import IO
from turbine.types import Document
from abc import abstractmethod


class FileParser:
    mime: str

    @abstractmethod
    def get_documents(self, file: IO) -> list[Document]:
        ...
