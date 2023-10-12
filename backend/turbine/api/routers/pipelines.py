from fastapi import APIRouter, HTTPException
from typing import List
from turbine.db.models import Pipeline
from turbine.schema import PipelineSchema, ExistingPipelineSchema
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID

router = APIRouter(prefix="/pipelines")


@router.post("/", status_code=201)
async def create_pipeline(pipeline: PipelineSchema):
    pipeline_instance = Pipeline.create(
        name=pipeline.name,
        description=pipeline.description,
        index_=pipeline.index,
        data_source=pipeline.data_source.model_dump(),
    )

    return {
        "message": "Pipeline created",
        "id": str(pipeline_instance.id),
    }


@router.get("/", response_model=List[ExistingPipelineSchema])
async def get_pipelines(user=Depends(get_user)):
    return [
        pipeline.dump()
        for pipeline in Pipeline.select().where(Pipeline.index_.user == user)
    ]


@router.get("/{id}", response_model=ExistingPipelineSchema)
async def get_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = Pipeline.get_or_none(Pipeline.id == id, Pipeline.index_.user == user)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline.dump()


@router.delete("/{pipeline_id}")
async def delete_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = Pipeline.get_or_none(Pipeline.id == id, Pipeline.index_.user == user)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    pipeline.delete_instance()
    return {"message": "Pipeline deleted"}
