from .auth import get_user
from logging import getLogger
import logging
from .routers import indices, tasks, pipelines
from fastapi import FastAPI, Depends, Request
from turbine.db import User

logger = getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
)

app = FastAPI(
    dependencies=[Depends(get_user)],
)


app.include_router(indices.router)
app.include_router(tasks.router)
app.include_router(pipelines.router)


@app.post("/webhooks/clerk")
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
