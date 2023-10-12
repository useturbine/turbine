from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from turbine.data_source import S3TextDataSource


class PipelineSchema(BaseModel):
    name: str
    description: Optional[str] = None
    index: UUID
    data_source: S3TextDataSource


class ExistingPipelineSchema(PipelineSchema):
    id: UUID
