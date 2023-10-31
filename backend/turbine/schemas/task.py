from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: UUID
    pipeline: Optional[UUID] = None
    index: Optional[UUID] = None
    created_at: datetime
    finished_at: Optional[datetime]
    successful: bool
