from fastapi import APIRouter
from turbine.database import Task, User, Pipeline
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException
from typing import Optional
from uuid import UUID


router = APIRouter(
    prefix="/tasks",
)


@router.get("/")
async def get_tasks(pipeline: Optional[UUID] = None, user=Depends(get_user)):
    if pipeline:
        tasks = (
            Task.select()
            .join(Pipeline)
            .where(
                Pipeline.id == pipeline,
                Pipeline.user == user,
                Pipeline.deleted == False,
            )
        )
    else:
        tasks = (
            Task.select()
            .join(Pipeline)
            .where(
                Pipeline.user == user,
                Pipeline.deleted == False,
            )
        )
    return [task.dump() for task in tasks]


@router.get("/{id}")
async def get_task(id: UUID, user=Depends(get_user)):
    task = (
        Task.select()
        .join(Pipeline)
        .where(
            Task.id == id,
            Pipeline.user == user,
            Pipeline.deleted == False,
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.dump()
