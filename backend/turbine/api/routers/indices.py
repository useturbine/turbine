from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
from peewee import DataError, DoesNotExist
from turbine.api.auth import get_user
from turbine.db.models import Index
from turbine.schema import IndexSchema

logger = getLogger(__name__)
router = APIRouter(prefix="/indices")


@router.get("/")
def get_indices(user=Depends(get_user)):
    indices = Index.select().where(Index.user == user.id)
    return [index.dump() for index in indices]


@router.get("/{id}")
def get_index(id: str, user=Depends(get_user)):
    try:
        index = Index.get(Index.id == id, user=user.id)
    except (DoesNotExist, DataError):
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
        vector_db_type=index.vector_db.type,
        vector_db_config=index.vector_db.config.model_dump(),
        embedding_model_type=index.embedding_model.type,
        embedding_model_config=index.embedding_model.config.model_dump(),
        embedding_dimension=index.embedding_dimension,
        similarity_metric=index.similarity_metric,
    )

    vector_db = index.vector_db.config.get_instance()
    collection_name = vector_db.get_collection_name(index_instance.id)

    try:
        vector_db.create_collection(
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
def delete_index(id: str, user=Depends(get_user)):
    try:
        index = Index.get(Index.id == id, user=user.id)
    except (DoesNotExist, DataError):
        raise HTTPException(404, "Index not found")

    vector_db = index.dump().vector_db.get_instance()
    collection_name = vector_db.get_collection_name(index.id)

    index.delete_instance()
    vector_db.drop_collection(collection_name)

    return {"message": "Index deleted"}
