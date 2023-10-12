from .auth import get_user
from logging import getLogger
import logging
from .routers import indices, tasks, pipelines, misc
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


logger = getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
)


app = FastAPI(
    dependencies=[Depends(get_user)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(indices.router)
app.include_router(tasks.router)
app.include_router(pipelines.router)
app.include_router(misc.router)
