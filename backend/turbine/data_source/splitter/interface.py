from abc import abstractmethod
from typing import Optional
from pydantic import BaseModel
from typing import Any


class SplitterOutput(BaseModel):
    text: str
    metadata: dict[str, Any]


class Splitter:
    @abstractmethod
    def split(self, text: str) -> list[SplitterOutput]:
        ...
