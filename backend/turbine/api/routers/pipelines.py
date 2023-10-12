from fastapi import APIRouter, HTTPException
from typing import List
from turbine.db import Pipeline, Index, Task
from turbine.schema import PipelineSchema, ExistingPipelineSchema
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from peewee import IntegrityError
from turbine.worker import run_pipeline as run_pipeline_task

router = APIRouter(prefix="/pipelines")


@router.post("/", status_code=201)
async def create_pipeline(pipeline: PipelineSchema):
    try:
        pipeline_instance = Pipeline.create(
            name=pipeline.name,
            description=pipeline.description,
            index_=pipeline.index,
            data_source=pipeline.data_source.model_dump(),
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Index does not exist")

    return {
        "message": "Pipeline created",
        "id": str(pipeline_instance.id),
    }


@router.get("/", response_model=List[ExistingPipelineSchema])
async def get_pipelines(user=Depends(get_user)):
    return [
        pipeline.dump()
        for pipeline in Pipeline.select().join(Index).where(Index.user == user)
    ]


@router.get("/{id}", response_model=ExistingPipelineSchema)
async def get_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = (
        Pipeline.select()
        .join(Index)
        .where(Pipeline.id == id, Index.user == user)
        .first()
    )

    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline.dump()


@router.delete("/{id}")
async def delete_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = (
        Pipeline.select()
        .join(Index)
        .where(Pipeline.id == id, Index.user == user)
        .first()
    )
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    pipeline.delete_instance()
    return {"message": "Pipeline deleted"}


@router.post("/{id}/run")
async def run_pipeline(id: UUID, user=Depends(get_user)):
    pipeline_instance = (
        Pipeline.select()
        .join(Index)
        .where(Pipeline.id == id, Index.user == user)
        .first()
    )
    if not pipeline_instance:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    task = run_pipeline_task.delay(id)
    print("index id", pipeline_instance.index_)
    Task.create(
        id=task.id,
        index_=pipeline_instance.index_,
        kind="manual_pipeline_run",
    )
    return {"message": "Task has started running", "id": task.id}
