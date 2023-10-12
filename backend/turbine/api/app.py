from .auth import get_user
from logging import getLogger
import logging
from .routers import indices, tasks, pipelines
from fastapi import FastAPI, Depends


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
