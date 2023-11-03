from fastapi import APIRouter, HTTPException
from turbine.database import DataSource, User, get_db, Index
from turbine.schemas import DataSourceSchemaGet, DataSourceSchema
from turbine.api.auth import get_user
from fastapi import Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from prefect.client.orchestration import get_client
from turbine.flows import sync_data_source as sync_flow
from prefect.deployments.deployments import Deployment, run_deployment
from .utils import CreateResponseSchema, GenericResponseSchema
from typing import Optional


router = APIRouter(prefix="/data-sources")
prefect = get_client()


@router.post("", status_code=201, response_model=CreateResponseSchema)
async def create_data_source(
    data_source: DataSourceSchema,
    db: Session = Depends(get_db),
):
    stmt = select(Index).filter_by(id=data_source.index_id, deleted=False)
    index_instance = db.scalars(stmt).one_or_none()
    if not index_instance:
        raise HTTPException(status_code=404, detail="Index not found")
    index = index_instance.dump()

    try:
        data_source.validate_config()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data_source_instance = DataSource(
        name=data_source.name,
        data_source=data_source.data_source.model_dump(),
        index_id=data_source.index_id,
    )
    db.add(data_source_instance)
    db.flush()

    await Deployment.build_from_flow(
        sync_flow,
        name=str(data_source_instance.id),
        parameters={
            "data_source": data_source.model_dump(),
            "index": index.model_dump(),
        },
        apply=True,
    )

    db.commit()
    return {
        "message": "Data source created",
        "id": str(data_source_instance.id),
    }


@router.get("", response_model=list[DataSourceSchemaGet])
async def get_data_sources(
    index_id: Optional[UUID] = None,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(DataSource)
        .join(Index)
        .where(Index.user_id == user.id, DataSource.deleted == False)
    )
    if index_id:
        stmt = stmt.where(DataSource.index_id == index_id)
    data_sources = db.scalars(stmt).all()
    return [data_source.dump() for data_source in data_sources]


@router.get("/{id}", response_model=DataSourceSchemaGet)
async def get_data_source(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(DataSource)
        .join(Index)
        .where(
            DataSource.id == id, Index.user_id == user.id, DataSource.deleted == False
        )
    )
    data_source = db.scalars(stmt).one_or_none()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return data_source.dump()


@router.delete("/{id}", response_model=GenericResponseSchema)
async def delete_data_source(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(DataSource)
        .join(Index)
        .where(
            DataSource.id == id, Index.user_id == user.id, DataSource.deleted == False
        )
    )
    data_source = db.scalars(stmt).one_or_none()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")

    deployment = await prefect.read_deployment_by_name("sync-data-source/" + str(id))
    await prefect.delete_deployment(deployment.id)

    data_source.deleted = True
    db.commit()
    return {"message": "Data source deleted"}


@router.post("/{id}/run", response_model=CreateResponseSchema)
async def sync_data_source(
    id: UUID, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    stmt = (
        select(DataSource)
        .join(Index)
        .where(
            DataSource.id == id, Index.user_id == user.id, DataSource.deleted == False
        )
    )
    data_source = db.scalars(stmt).one_or_none()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")

    result = await run_deployment("sync-data-source/" + str(id), timeout=0)
    return {"message": "Task has started running", "id": result.id}
