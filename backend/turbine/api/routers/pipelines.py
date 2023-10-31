from fastapi import APIRouter, HTTPException
from turbine.database import Pipeline, User, get_db, Index
from turbine.schemas import PipelineSchema, PipelineSchemaGet
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from prefect.client.orchestration import get_client
from turbine.flows import run_pipeline as pipeline_flow
from prefect.deployments.deployments import Deployment, run_deployment
from .utils import CreateResponseSchema, GenericResponseSchema
from typing import Optional


router = APIRouter(prefix="/pipelines")
prefect = get_client()


@router.post("", status_code=201, response_model=CreateResponseSchema)
async def create_pipeline(
    pipeline: PipelineSchema,
    db: Session = Depends(get_db),
):
    stmt = select(Index).filter_by(id=pipeline.index_id, deleted=False)
    index_instance = db.scalars(stmt).one_or_none()
    if not index_instance:
        raise HTTPException(status_code=404, detail="Index not found")
    index = index_instance.dump()

    try:
        pipeline.validate_config()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    pipeline_instance = Pipeline(
        name=pipeline.name,
        data_source=pipeline.data_source.model_dump(),
        index_id=pipeline.index_id,
    )
    db.add(pipeline_instance)
    db.flush()

    await Deployment.build_from_flow(
        pipeline_flow,
        name=str(pipeline_instance.id),
        parameters={"pipeline": pipeline.model_dump(), "index": index.model_dump()},
        apply=True,
    )

    db.commit()
    return {
        "message": "Pipeline created",
        "id": str(pipeline_instance.id),
    }


@router.get("", response_model=list[PipelineSchemaGet])
async def get_pipelines(
    index_id: Optional[UUID] = None,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Pipeline)
        .join(Index)
        .where(Index.user_id == user.id, Pipeline.deleted == False)
    )
    if index_id:
        stmt = stmt.where(Pipeline.index_id == index_id)
    pipelines = db.scalars(stmt).all()
    return [pipeline.dump() for pipeline in pipelines]


@router.get("/{id}", response_model=PipelineSchemaGet)
async def get_pipeline(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(Pipeline)
        .join(Index)
        .where(Pipeline.id == id, Index.user_id == user.id, Pipeline.deleted == False)
    )
    pipeline = db.scalars(stmt).one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline.dump()


@router.delete("/{id}", response_model=GenericResponseSchema)
async def delete_pipeline(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(Pipeline)
        .join(Index)
        .where(Pipeline.id == id, Index.user_id == user.id, Pipeline.deleted == False)
    )
    pipeline = db.scalars(stmt).one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    deployment = await prefect.read_deployment_by_name(str(id))
    await prefect.delete_deployment(deployment.id)

    pipeline.deleted = True
    db.commit()
    return {"message": "Pipeline deleted"}


@router.post("/{id}/run", response_model=CreateResponseSchema)
async def run_pipeline(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(Pipeline)
        .join(Index)
        .where(Pipeline.id == id, Index.user_id == user.id, Pipeline.deleted == False)
    )
    pipeline_instance = db.scalars(stmt).one_or_none()
    if not pipeline_instance:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    result = await run_deployment("run-pipeline/" + str(id), timeout=0)
    return {"message": "Task has started running", "id": result.id}
