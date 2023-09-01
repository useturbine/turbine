from fastapi import FastAPI, Depends, HTTPException
from .schema import Project as ProjectSchema
from src.db.models import Project, Log
from .auth import get_user
from logging import getLogger
from src.datasource.debezium.debezium import DebeziumDataSource
from src.vectordb.milvus import MilvusVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config
import json
from typing import Optional


logger = getLogger(__name__)
app = FastAPI()

debezium = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)
vector_db = MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)
embedding_model = OpenAIModel(api_key=Config.openai_api_key)


@app.post("/v1/projects")
def create_project(project: ProjectSchema, user=Depends(get_user)):
    project_instance = Project.create(config=project.model_dump(), user=user)

    try:
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
            f"turbine{project_instance.id}", OpenAIModel.embedding_dimension
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
    return {"message": f"Project {project_instance.id} added successfully"}, 201


@app.get("/v1/projects")
def get_projects(id: Optional[str] = None, user=Depends(get_user)):
    if id:
        project = Project.get_or_none(Project.id == id, Project.user == user)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project.to_dict(), 200

    return [p.to_dict() for p in Project.select().where(Project.user == user)], 200


@app.delete("/v1/projects")
def delete_project(id: str, user=Depends(get_user)):
    project = Project.get_or_none(Project.id == id, Project.user == user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.delete_instance()
    debezium.delete_connector(project.id)
    vector_db.drop_collection(f"turbine_{project.id}")

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


@app.put("/v1/projects")
def update_project(id: str, project: ProjectSchema, user=Depends(get_user)):
    project_instance = Project.get_or_none(Project.id == id, Project.user == user)
    if not project_instance:
        raise HTTPException(status_code=404, detail="Project not found")

    project_instance.config = project.model_dump_json()
    project_instance.save()

    try:
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
            f"turbine{project_instance.id}", OpenAIModel.embedding_dimension
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
                "action": "update_project",
                "user": user.id,
                "project": project_instance.id,
            }
        ),
    )
    logger.info(f"Updated project {project_instance.id} for user {user.id}")
    return {"message": f"Project {project_instance.id} updated successfully"}, 200


@app.get("/v1/projects/{project_id}/search")
def search(project_id: str, query: str, limit: int = 10, user=Depends(get_user)):
    project = Project.get_or_none(Project.id == project_id, Project.user == user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    results = vector_db.search(
        collection_name=f"turbine{project.id}",
        data=embedding_model.get_embedding(query),
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
