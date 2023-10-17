from turbine.database import User
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from uuid import UUID
from turbine.database import get_db
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
from sqlalchemy import select


auth_scheme = APIKeyHeader(name="X-Turbine-Key", auto_error=False)


async def get_user(
    api_key: UUID = Depends(auth_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    try:
        stmt = select(User).filter(User.api_key == api_key, User.deleted == False)
        user = db.scalars(stmt).one_or_none()
    except DataError:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user
