from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
from peewee import DataError, DoesNotExist
from turbine.api.auth import get_user
from turbine.db import Index
from turbine.schema import ExistingIndexSchema, IndexSchema
from uuid import UUID
from turbine.vector_db import VectorDB

logger = getLogger(__name__)
router = APIRouter(prefix="/indices")


@router.get("/")
def get_indices(user=Depends(get_user)):
    return [index.dump() for index in Index.select().where(Index.user == user)]


@router.get("/{id}")
def get_index(id: UUID, user=Depends(get_user)):
    index = Index.get_or_none(Index.id == id, user == user)
    if not index:
        raise HTTPException(404, "Index not found")
    return index.dump()


@router.post("/", status_code=201)
def create_index(
    index: IndexSchema,
    user=Depends(get_user),
):
    index_instance = Index.create(
        user=user,
        name=index.name,
        description=index.description,
        vector_db=index.vector_db.model_dump(),
        embedding_model=index.embedding_model.model_dump(),
        embedding_dimension=index.embedding_dimension,
        similarity_metric=index.similarity_metric,
    )

    collection_name = index.vector_db.get_collection_name(index_instance.id)

    try:
        index.vector_db.create_collection(
            collection_name,
            index.embedding_dimension,
            index.similarity_metric,
        )
    except Exception as e:
        logger.error(e)
        index_instance.delete_instance()
        raise HTTPException(status_code=400, detail="Failed to add index")

    return {
        "message": "Index created",
        "id": str(index_instance.id),
    }


@router.delete("/{id}")
def delete_index(id: UUID, user=Depends(get_user)):
    try:
        index = Index.get(Index.id == id, user=user.id)
    except (DoesNotExist, DataError):
        raise HTTPException(404, "Index not found")

    vector_db: VectorDB = index.dump().vector_db
    collection_name = vector_db.get_collection_name(index.id)

    index.delete_instance()
    vector_db.drop_collection(collection_name)

    return {"message": "Index deleted"}


@router.get("/{id}/search")
def search_index(id: UUID, query: str, limit: int = 10, user=Depends(get_user)):
    index_instance = Index.get_or_none(Index.id == id, user=user.id)
    if not index_instance:
        raise HTTPException(404, "Index not found")

    index: ExistingIndexSchema = index_instance.dump()
    collection_name = index.vector_db.get_collection_name(index.id)

    query_embedding = index.embedding_model.get_embedding(query)
    return index.vector_db.search(collection_name, query_embedding, limit=limit)
