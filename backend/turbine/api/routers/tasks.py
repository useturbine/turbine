from fastapi import APIRouter
from turbine.database import Pipeline, get_db, User
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException
from typing import Optional
from uuid import UUID
from turbine.schema import TaskSchema
from sqlalchemy.orm import Session
from sqlalchemy import select
from prefect import get_client
from prefect.exceptions import ObjectNotFound
from prefect.client.schemas.filters import DeploymentFilter
from prefect.client.schemas.sorting import FlowRunSort


router = APIRouter(
    prefix="/tasks",
)
prefect = get_client()


@router.get("", response_model=list[TaskSchema])
async def get_tasks(
    pipeline: Optional[UUID] = None,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    stmt = select(Pipeline).where(
        Pipeline.user_id == user.id, Pipeline.deleted == False
    )
    if pipeline:
        stmt = stmt.where(Pipeline.id == pipeline)
    pipelines = db.scalars(stmt).all()

    flow_runs = await prefect.read_flow_runs(
        deployment_filter=DeploymentFilter(
            name={"_any": [str(pipeline.id) for pipeline in pipelines]}
        ),
        sort=FlowRunSort.START_TIME_DESC,
    )

    tasks = []
    for flow_run in flow_runs:
        if (
            not flow_run.deployment_id
            or not flow_run.state
            or not flow_run.expected_start_time
        ):
            continue
        deployment = await prefect.read_deployment(flow_run.deployment_id)
        pipeline_id = UUID(deployment.name)

        tasks.append(
            TaskSchema(
                id=flow_run.id,
                pipeline=pipeline_id,
                created_at=flow_run.expected_start_time,
                finished_at=flow_run.end_time,
                successful=flow_run.state.is_completed(),
            )
        )

    return tasks


@router.get("/{id}", response_model=TaskSchema)
async def get_task(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    try:
        flow_run = await prefect.read_flow_run(id)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    if (
        not flow_run.deployment_id
        or not flow_run.state
        or not flow_run.expected_start_time
    ):
        raise HTTPException(status_code=404, detail="Task not found")

    deployment = await prefect.read_deployment(flow_run.deployment_id)
    pipeline_id = UUID(deployment.name)
    pipeline = db.scalars(select(Pipeline).where(Pipeline.id == pipeline_id)).first()
    if not pipeline or pipeline.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskSchema(
        id=flow_run.id,
        pipeline=pipeline_id,
        created_at=flow_run.expected_start_time,
        finished_at=flow_run.end_time,
        successful=flow_run.state.is_completed(),
    )
