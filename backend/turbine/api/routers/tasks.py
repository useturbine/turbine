from fastapi import APIRouter
from turbine.db import Task, User, Index
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException
from typing import Optional


router = APIRouter(
    prefix="/tasks",
)


@router.get("/")
async def get_tasks(index: Optional[str] = None, user=Depends(get_user)):
    if index:
        tasks = (
            Task.select()
            .join(Index)
            .join(User)
            .where(User.id == user.id, Index.id == index)
        )
    else:
        tasks = Task.select().join(Index).join(User).where(User.id == user.id)
    return [task.dump() for task in tasks]


@router.get("/{id}")
async def get_task(id: str, user=Depends(get_user)):
    task = (
        Task.select()
        .join(Index)
        .join(User)
        .where(User.id == user.id, Task.id == id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.dump()
