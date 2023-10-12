from turbine.db import User
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import Annotated


auth_scheme = APIKeyHeader(name="X-Turbine-Key", auto_error=False)


def get_user(turbine_key: Annotated[str, Depends(auth_scheme)]) -> User:
    if not turbine_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    user = User.get_or_none(User.api_key == turbine_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user
