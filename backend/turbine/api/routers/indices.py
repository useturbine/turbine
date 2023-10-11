from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
from peewee import DataError, DoesNotExist
from turbine.api.auth import get_user
from turbine.db.models import Index as IndexModel
from turbine.schema import Index as IndexSchema

logger = getLogger(__name__)
router = APIRouter(prefix="/indices")


@router.get("/")
def get_indices(user=Depends(get_user)):
    indices = IndexModel.select().where(IndexModel.user == user.id)
    return [index.dump() for index in indices]


@router.get("/{id}")
def get_index(id: str, user=Depends(get_user)):
    try:
        index = IndexModel.get(IndexModel.id == id, user=user.id)
    except (DoesNotExist, DataError):
        raise HTTPException(404, "Index not found")
    return index.dump()


@router.post("/", status_code=201)
def create_index(
    index: IndexSchema,
    user=Depends(get_user),
):
    index_instance = IndexModel.create(
        user=user,
        name=index.name,
        description=index.description,
        vector_db=index.vector_db,
        embedding_model=index.embedding_model,
    )
    return index_instance.dump()
