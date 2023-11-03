from fastapi import APIRouter
from turbine.database import Pipeline, get_db, User, Index
from turbine.api.auth import get_user
from fastapi import Depends, HTTPException
from typing import Optional
from uuid import UUID
from turbine.schemas import TaskSchema
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
    pipeline_id: Optional[UUID] = None,
    index_id: Optional[UUID] = None,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    if pipeline_id and index_id:
        raise HTTPException(
            status_code=400, detail="Only one of pipeline_id or index_id is allowed"
        )

    stmt = (
        select(Pipeline)
        .join(Index)
        .where(Index.user_id == user.id, Pipeline.deleted == False)
    )
    if pipeline_id:
        stmt = stmt.where(Pipeline.id == pipeline_id)
    pipelines = db.scalars(stmt).all()

    stmt = select(Index).where(Index.user_id == user.id, Index.deleted == False)
    if index_id:
        stmt = stmt.where(Index.id == index_id)
    indexes = db.scalars(stmt).all()

    if pipeline_id:
        deployment_names = [str(pipeline.id) for pipeline in pipelines]
    elif index_id:
        deployment_names = [str(index.id) for index in indexes]
    else:
        deployment_names = [str(index.id) for index in indexes] + [
            str(pipeline.id) for pipeline in pipelines
        ]

    flow_runs = await prefect.read_flow_runs(
        deployment_filter=DeploymentFilter(
            name={
                "_any": deployment_names,
            }
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
        tasks.append(
            TaskSchema(
                id=flow_run.id,
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
    deployment_id = UUID(deployment.name)

    stmt = (
        select(Pipeline)
        .join(Index)
        .where(
            Pipeline.id == deployment_id,
            Index.user_id == user.id,
            Pipeline.deleted == False,
        )
    )
    pipeline = db.scalars(stmt).one_or_none()
    if pipeline:
        return TaskSchema(
            id=flow_run.id,
            pipeline_id=deployment_id,
            created_at=flow_run.expected_start_time,
            finished_at=flow_run.end_time,
            successful=flow_run.state.is_completed(),
        )

    stmt = select(Index).where(
        Index.id == deployment_id,
        Index.user_id == user.id,
        Index.deleted == False,
    )
    index = db.scalars(stmt).one_or_none()
    if index:
        return TaskSchema(
            id=flow_run.id,
            index_id=deployment_id,
            created_at=flow_run.expected_start_time,
            finished_at=flow_run.end_time,
            successful=flow_run.state.is_completed(),
        )

    raise HTTPException(status_code=404, detail="Task not found")
