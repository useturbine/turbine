from fastapi import APIRouter, Request
from turbine.database import User
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from turbine.database import get_db
from fastapi import Depends


router = APIRouter()


@router.post("/webhooks/clerk", include_in_schema=False)
async def clerk_webhook(request: Request, db: Session = Depends(get_db)):
    request_body = await request.json()

    if request_body["type"] == "user.created" or request_body["type"] == "user.deleted":
        user_id = request_body["data"]["id"]
    elif request_body["type"] == "session.created":
        user_id = request_body["data"]["user_id"]
    else:
        return {"message": "Webhook processed"}

    stmt = select(User).where(User.clerk_id == user_id, User.deleted == False)
    user = db.scalars(stmt).one_or_none()
    if not user:
        user = User(clerk_id=user_id)
        db.add(user)

    if request_body["type"] == "user.deleted":
        user.deleted = True

    db.commit()
    return {"message": "Webhook processed"}


@router.get("/users/{clerk_id}", include_in_schema=False)
async def get_user(clerk_id: str, db: Session = Depends(get_db)):
    stmt = select(User).where(User.clerk_id == clerk_id, User.deleted == False)
    user = db.scalars(stmt).one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return {"api_key": str(user.api_key)}
