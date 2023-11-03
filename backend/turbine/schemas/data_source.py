from pydantic import BaseModel
from uuid import UUID
from turbine.data_sources import S3


DataSource = S3


class DataSourceSchema(BaseModel):
    name: str
    index_id: UUID
    data_source: DataSource

    def validate_config(self) -> None:
        self.data_source.validate_config()


class DataSourceSchemaGet(DataSourceSchema):
    id: UUID
