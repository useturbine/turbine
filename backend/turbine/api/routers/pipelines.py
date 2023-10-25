from fastapi import APIRouter, HTTPException
from typing import List
from turbine.database import Pipeline, User, get_db
from turbine.schema import PipelineSchema, PipelineSchemaGet
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from pydantic import BaseModel
from turbine.vector_database import VectorSearchResult
from sqlalchemy.orm import Session
from sqlalchemy import select
from prefect.client.orchestration import get_client
from turbine.flows import run_pipeline as pipeline_flow
from prefect.deployments.deployments import Deployment, run_deployment


router = APIRouter(prefix="/pipelines")
prefect = get_client()


class CreateResponseSchema(BaseModel):
    message: str
    id: UUID


class GenericResponseSchema(BaseModel):
    message: str


@router.post("", status_code=201, response_model=CreateResponseSchema)
async def create_pipeline(
    pipeline: PipelineSchema,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    try:
        pipeline.validate_config()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    pipeline_instance = Pipeline(
        name=pipeline.name,
        description=pipeline.description,
        data_source=pipeline.data_source.model_dump(),
        vector_database=pipeline.vector_database.model_dump(),
        embedding_model=pipeline.embedding_model.model_dump(),
        user_id=user.id,
    )
    db.add(pipeline_instance)
    db.flush()

    await Deployment.build_from_flow(
        pipeline_flow,
        name=str(pipeline_instance.id),
        parameters={"pipeline": pipeline.model_dump()},
        apply=True,
    )

    db.commit()
    return {
        "message": "Pipeline created",
        "id": str(pipeline_instance.id),
    }


@router.get("", response_model=List[PipelineSchemaGet])
async def get_pipelines(user: User = Depends(get_user), db: Session = Depends(get_db)):
    stmt = select(Pipeline).filter_by(user_id=user.id, deleted=False)
    pipelines = db.scalars(stmt).all()
    return [pipeline.dump() for pipeline in pipelines]


@router.get("/{id}", response_model=PipelineSchemaGet)
async def get_pipeline(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = select(Pipeline).filter_by(id=id, user_id=user.id, deleted=False)
    pipeline = db.scalars(stmt).one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline.dump()


@router.delete("/{id}", response_model=GenericResponseSchema)
async def delete_pipeline(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = select(Pipeline).filter_by(id=id, user_id=user.id, deleted=False)
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
    stmt = select(Pipeline).filter_by(id=id, user_id=user.id, deleted=False)
    pipeline_instance = db.scalars(stmt).one_or_none()
    if not pipeline_instance:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    result = await run_deployment("run-pipeline/" + str(id), timeout=0)
    return {"message": "Task has started running", "id": result.id}


@router.get("/{id}/search", response_model=list[VectorSearchResult])
async def search(
    id: UUID,
    query: str,
    limit: int = 10,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    stmt = select(Pipeline).filter_by(id=id, user_id=user.id, deleted=False)
    pipeline_instance = db.scalars(stmt).one_or_none()
    if not pipeline_instance:
        raise HTTPException(404, "Pipeline not found")

    pipeline: PipelineSchema = pipeline_instance.dump()
    query_embedding = pipeline.embedding_model.get_embeddings([query])[0]
    results = pipeline.vector_database.search(query_embedding, limit=limit)
    return results
