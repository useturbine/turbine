from celery.result import AsyncResult
from fastapi import APIRouter
from turbine.worker import app
from turbine.db.models import Task
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException


router = APIRouter(
    prefix="/tasks",
)


def get_task_details(task_id: str):
    task = AsyncResult(task_id, app=app)
    return {
        "id": task_id,
        "status": task.status,
        "result": task.result,
        "info": task.info,
    }


@router.get("/")
async def get_tasks(user=Depends(get_user)):
    tasks = Task.select().where(Task.index_.user == user)
    return [get_task_details(task.id) for task in tasks]


@router.get("/{id}")
async def get_task(id: str, user=Depends(get_user)):
    task = Task.get_or_none(Task.id == id, Task.index_.user == user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return get_task_details(task.id)
