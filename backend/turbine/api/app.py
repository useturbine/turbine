from fastapi import FastAPI, Depends, HTTPException
from turbine.schema import Project as ProjectSchema
from turbine.db.models import Project, Log
from .auth import get_user
from logging import getLogger
from turbine.data_source.debezium.debezium import DebeziumDataSource
from config import Config
import json
from typing import Optional
from turbine.utils import get_vector_db
import logging
from .routers import indices

logger = getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
)

app = FastAPI()
app.include_router(indices.router)

debezium = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)


@app.get("/v1/projects")
@app.get("/v1/projects/{id}")
def get_projects(id: Optional[str] = None, user=Depends(get_user)):
    if id:
        project = Project.get_or_none(Project.id == id, Project.user == user)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project.to_dict()

    return [p.to_dict() for p in Project.select().where(Project.user == user)]


@app.delete("/v1/projects/{id}")
def delete_project(id: str, user=Depends(get_user)):
    project = Project.get_or_none(Project.id == id, Project.user == user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    vector_db = get_vector_db(project.config["vector_db"])

    project.delete_instance()
    debezium.delete_connector(project.id)
    vector_db.drop_collection(f"turbine{project.id}")

    Log.create(
        user=user,
        info=json.dumps(
            {
                "action": "delete_project",
                "user": user.id,
                "project": project.id,
            }
        ),
    )
    logger.info(f"Deleted project {project.id} for user {user.id}")
    return {"message": f"Project {project.id} deleted successfully"}
