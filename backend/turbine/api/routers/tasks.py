from celery.result import AsyncResult
from fastapi import APIRouter
from turbine.worker import app
from turbine.db.models import Task, User, Index
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException


router = APIRouter(
    prefix="/tasks",
)


def get_task_details(task):
    task_result = AsyncResult(task.id, app=app)
    if task_result.ready() and task.finished_at is None:
        task.finished_at = task_result.date_done
        task.save()

    return {
        "id": task.id,
        "kind": task.kind,
        "status": task_result.status,
        "created_at": task.created_at,
        "finished_at": task.finished_at,
    }


@router.get("/")
async def get_tasks(user=Depends(get_user)):
    tasks = Task.select().join(Index).join(User).where(User.id == user.id)
    return [get_task_details(task) for task in tasks]


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
    return get_task_details(task)
