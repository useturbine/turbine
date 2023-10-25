from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: UUID
    pipeline: UUID
    created_at: datetime
    finished_at: Optional[datetime]
    successful: bool
