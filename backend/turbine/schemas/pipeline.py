from pydantic import BaseModel
from uuid import UUID
from turbine.data_sources import S3


DataSource = S3


class PipelineSchema(BaseModel):
    name: str
    data_source: DataSource
    index_id: UUID

    def validate_config(self) -> None:
        self.data_source.validate_config()


class PipelineSchemaGet(PipelineSchema):
    id: UUID
