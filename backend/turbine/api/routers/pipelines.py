from fastapi import APIRouter, HTTPException
from typing import List
from turbine.database import Pipeline, Task
from turbine.schema import PipelineSchema, ExistingPipelineSchema
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from turbine.worker import run_pipeline as run_pipeline_task
from pydantic import BaseModel
from turbine.vector_database import VectorSearchResult


router = APIRouter(prefix="/pipelines")


class CreateResponseSchema(BaseModel):
    message: str
    id: UUID


class GenericResponseSchema(BaseModel):
    message: str


@router.post("", status_code=201, response_model=CreateResponseSchema)
async def create_pipeline(pipeline: PipelineSchema, user=Depends(get_user)):
    pipeline_instance = Pipeline.create(
        name=pipeline.name,
        description=pipeline.description,
        data_source=pipeline.data_source.model_dump(),
        vector_database=pipeline.vector_database.model_dump(),
        embedding_model=pipeline.embedding_model.model_dump(),
        user=user,
    )
    return {
        "message": "Pipeline created",
        "id": str(pipeline_instance.id),
    }


@router.get("", response_model=List[ExistingPipelineSchema])
async def get_pipelines(user=Depends(get_user)):
    pipelines = Pipeline.select().where(
        Pipeline.user == user, Pipeline.deleted == False
    )
    return [pipeline.dump() for pipeline in pipelines]


@router.get("/{id}", response_model=ExistingPipelineSchema)
async def get_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = Pipeline.get_or_none(
        Pipeline.id == id, Pipeline.user == user, Pipeline.deleted == False
    )
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline.dump()


@router.delete("/{id}", response_model=GenericResponseSchema)
async def delete_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = Pipeline.get_or_none(Pipeline.id == id, Pipeline.user == user)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    pipeline.deleted = True
    pipeline.save()
    return {"message": "Pipeline deleted"}


@router.post("/{id}/run", response_model=CreateResponseSchema)
async def run_pipeline(id: UUID, user=Depends(get_user)):
    pipeline = Pipeline.get_or_none(
        Pipeline.id == id, Pipeline.user == user, Pipeline.deleted == False
    )
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    task = Task.create(
        pipeline=pipeline,
        type="manual_pipeline_run",
    )
    try:
        run_pipeline_task.delay(id, task.id)
    except Exception as e:
        task.delete_instance()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Task has started running", "id": task.id}


@router.get("/{id}/search", response_model=list[VectorSearchResult])
def search(id: UUID, query: str, limit: int = 10, user=Depends(get_user)):
    pipeline_instance = Pipeline.get_or_none(
        Pipeline.id == id, Pipeline.user == user, Pipeline.deleted == False
    )
    if not pipeline_instance:
        raise HTTPException(404, "Pipeline not found")

    pipeline: ExistingPipelineSchema = pipeline_instance.dump()
    query_embedding = pipeline.embedding_model.get_embedding(query)
    results = pipeline.vector_database.search(query_embedding, limit=limit)
    return results
