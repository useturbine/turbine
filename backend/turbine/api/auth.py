from turbine.database import User
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import Annotated
from uuid import UUID
from peewee import DataError


auth_scheme = APIKeyHeader(name="X-Turbine-Key", auto_error=False)


async def get_user(turbine_key: Annotated[UUID, Depends(auth_scheme)]) -> User:
    if not turbine_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    try:
        user = User.get_or_none(User.api_key == turbine_key, User.deleted == False)
    except DataError:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user
