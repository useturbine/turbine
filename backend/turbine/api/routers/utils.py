from pydantic import BaseModel
from uuid import UUID


class CreateResponseSchema(BaseModel):
    message: str
    id: UUID


class GenericResponseSchema(BaseModel):
    message: str
