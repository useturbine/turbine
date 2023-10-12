from fastapi import APIRouter, Request
from turbine.db import User
from fastapi import HTTPException


router = APIRouter()


@router.post("/webhooks/clerk")
async def clerk_webhook(request: Request):
    request_body = await request.json()
    print(request_body, request.headers)

    if request_body["type"] == "user.created":
        User.create(
            external_id=request_body["data"]["id"],
        )
    elif request_body["type"] == "user.deleted":
        User.delete().where(User.external_id == request_body["data"]["id"])

    return {"message": "Webhook processed"}


@router.get("/users/{external_id}")
async def get_user(external_id: str):
    user = User.get_or_none(User.external_id == external_id, User.deleted == False)
    if not user:
        raise HTTPException(404, "User not found")
    return {"api_key": str(user.api_key)}
