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
from turbine.embedding_model import get_embedding_model
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


@app.post("/v1/projects", status_code=201)
def create_project(project: ProjectSchema, user=Depends(get_user)):
    project_instance = Project.create(config=project.model_dump(), user=user)

    vector_db = get_vector_db(project.vector_db)
    embedding_model = get_embedding_model(project.embedding_model)

    try:
        if project.data_source.type in ["mongo", "postgres"]:
            debezium.add_connector(
                id=project_instance.id,
                type=project.data_source.type,
                config=project.data_source.config,
            )
    except Exception as e:
        project_instance.delete_instance()
        logger.info(f"Failed to add connector to debezium: {e}")
        raise HTTPException(status_code=400, detail="Invalid data source config")

    try:
        vector_db.create_collection(
            f"turbine{project_instance.id}",
            embedding_model.dimensions,
            embedding_model.similarity_metric,
        )
    except Exception as e:
        project_instance.delete_instance()
        debezium.delete_connector(project_instance.id)
        logger.info(f"Failed to create vector DB: {e}")
        raise HTTPException(status_code=400, detail="Failed to create vector DB")

    Log.create(
        user=user,
        info=json.dumps(
            {
                "action": "add_project",
                "user": user.id,
                "project": project_instance.id,
            }
        ),
    )
    logger.info(f"Added project {project_instance.id} for user {user.id}")
    return {"message": f"Project created successfully", "id": project_instance.id}


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


@app.get("/v1/projects/{project_id}/search")
def search(project_id: str, query: str, limit: int = 10, user=Depends(get_user)):
    project = Project.get_or_none(Project.id == project_id, Project.user == user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    vector_db = get_vector_db(project.config["vector_db"])
    embedding_model = get_embedding_model(project.config["embedding_model"])

    results = vector_db.search(
        collection_name=f"turbine{project.id}",
        data=embedding_model.model.get_embedding(query),
        limit=limit,
    )

    Log.create(
        user=user,
        info=json.dumps(
            {
                "action": "search",
                "user": user.id,
                "project": project.id,
                "query": query,
                "limit": limit,
                "num_results": len(results),
            }
        ),
    )
    logger.info(
        f"User {user.id} searched for {query} in project {project.id} and got {len(results)} results"
    )
    return results
