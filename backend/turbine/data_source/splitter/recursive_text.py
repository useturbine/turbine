from pydantic import BaseModel
from typing import Literal
from .interface import Splitter, SplitterOutput
from langchain.text_splitter import RecursiveCharacterTextSplitter


class RecursiveSplitter(Splitter, BaseModel):
    type: Literal["recursive"]
    size: int
    overlap: int
    _splitter: RecursiveCharacterTextSplitter

    class Config:
        underscore_attrs_are_private = True

    def __init__(self, **data):
        super().__init__(**data)
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.size,
            chunk_overlap=self.overlap,
            add_start_index=True,
        )

    def split(self, text: str) -> list[SplitterOutput]:
        return [
            SplitterOutput(text=page.page_content, metadata=page.metadata)
            for page in self._splitter.create_documents([text])
        ]
