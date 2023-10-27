from .auth import get_user
from logging import getLogger
import logging
from .routers import tasks, pipelines, misc
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from turbine.database import Session, User
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
import sentry_sdk
from config import config


logger = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

sentry_sdk.init(
    dsn=config.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session() as db:
        user = User(api_key="b4f9137a-81bc-4acf-ae4e-ee33bef63dec", internal=True)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            pass
        yield


app = FastAPI(
    dependencies=[Depends(get_user)],
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://console.useturbine.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(pipelines.router)
app.include_router(misc.router)
