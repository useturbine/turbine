from pydantic import BaseModel
from typing import Literal, Optional
from uuid import UUID


class RecursiveSplitter(BaseModel):
    type: Literal["recursive"]
    size: int
    overlap: int


class S3TextDataSource(BaseModel):
    type: Literal["s3_text"]
    url: str
    splitter: RecursiveSplitter


class PipelineSchema(BaseModel):
    name: str
    description: Optional[str] = None
    index: UUID
    data_source: S3TextDataSource


class ExistingPipelineSchema(PipelineSchema):
    id: UUID
