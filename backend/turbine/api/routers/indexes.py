from fastapi import APIRouter, HTTPException
from typing import List
from turbine.database import User, get_db, Index, Pipeline
from turbine.schemas import IndexSchema, IndexSchemaGet
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from turbine.vector_databases import VectorSearchResult
from sqlalchemy.orm import Session
from sqlalchemy import select
from prefect.client.orchestration import get_client
from .utils import CreateResponseSchema, GenericResponseSchema


router = APIRouter(prefix="/indexes")
prefect = get_client()


@router.post("", status_code=201, response_model=CreateResponseSchema)
async def create_index(
    index: IndexSchema,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    try:
        index.validate_config()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    index_instance = Index(
        name=index.name,
        vector_database=index.vector_database.model_dump(),
        embedding_model=index.embedding_model.model_dump(),
        user_id=user.id,
    )
    db.add(index_instance)
    db.commit()

    return {
        "message": "Index created",
        "id": str(index_instance.id),
    }


@router.get("", response_model=List[IndexSchemaGet])
async def get_indexes(user: User = Depends(get_user), db: Session = Depends(get_db)):
    stmt = select(Index).filter_by(user_id=user.id, deleted=False)
    indexes = db.scalars(stmt).all()
    return [index.dump() for index in indexes]


@router.get("/{id}", response_model=IndexSchemaGet)
async def get_index(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = select(Index).filter_by(id=id, user_id=user.id, deleted=False)
    index = db.scalars(stmt).one_or_none()
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")
    return index.dump()


@router.delete("/{id}", response_model=GenericResponseSchema)
async def delete_index(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = select(Index).filter_by(id=id, user_id=user.id, deleted=False)
    index = db.scalars(stmt).one_or_none()
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")

    index.deleted = True
    db.add(index)

    stmt = select(Pipeline).filter_by(index_id=index.id, deleted=False)
    pipelines = db.scalars(stmt).all()
    for pipeline in pipelines:
        pipeline.deleted = True
        deployment = await prefect.read_deployment_by_name(str(id))
        await prefect.delete_deployment(deployment.id)
        db.add(pipeline)

    db.commit()
    return {"message": "Index deleted"}


@router.get("/{id}/search", response_model=list[VectorSearchResult])
async def search(
    id: UUID,
    query: str,
    limit: int = 10,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    stmt = select(Index).filter_by(id=id, user_id=user.id, deleted=False)
    index_instance = db.scalars(stmt).one_or_none()
    if not index_instance:
        raise HTTPException(404, "Index not found")

    index = index_instance.dump()
    query_embedding = index.embedding_model.get_embeddings([query])[0]
    results = index.vector_database.search(query_embedding, limit=limit)
    return results
