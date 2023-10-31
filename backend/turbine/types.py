from pydantic import BaseModel


Metadata = dict[str, str | int | list[str] | bool]


class Document(BaseModel):
    id: str
    content: str
    metadata: Metadata
