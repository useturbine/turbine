from .interface import FileParser
from typing import IO
from turbine.types import Document


class PDFParser(FileParser):
    mime = "application/pdf"

    def get_documents(self, file: IO) -> list[Document]:
        ...
