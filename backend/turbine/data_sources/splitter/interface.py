from abc import abstractmethod
from pydantic import BaseModel
from turbine.types import Metadata


class SplitterOutput(BaseModel):
    text: str
    metadata: Metadata


class Splitter:
    @abstractmethod
    def split(self, text: str) -> list[SplitterOutput]:
        ...
