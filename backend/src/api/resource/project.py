from flask_restful import Resource, reqparse
from src.api.auth import requires_auth, get_user
from src.db.models import ProjectModel, Log
from typing import Optional
from src.datasource.debezium.debezium import DebeziumDataSource
from src.vectordb.milvus import MilvusVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config
import json
import logging


logger = logging.getLogger(__name__)

parser = reqparse.RequestParser()
parser.add_argument(
    "config",
    type=dict,
    required=True,
    help="Configuration details for the data source cannot be blank",
)

debezium = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)
vector_db = MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)


class Project(Resource):
    @requires_auth
    def get(self, project_id: Optional[str] = None):
        user = get_user()
        if not project_id:
            return [
                p.to_dict()
                for p in ProjectModel.select().where(ProjectModel.user == user)
            ], 200

        project = ProjectModel.get_or_none(
            ProjectModel.id == project_id, ProjectModel.user == user
        )
        if not project:
            return {"error": f"Project ID {project_id} not found or user {user}"}, 404

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "get_data_source",
                    "user": user.id,
                    "project": project.id,
                }
            ),
        )
        logger.info(f"Retrieved data source {project.id} for user {user.id}")
        return project.to_dict(), 200

    @requires_auth
    def post(self):
        user = get_user()
        args = parser.parse_args()

        project = ProjectModel.create(
            type=args["type"], config=json.dumps(args["config"]), user=user
        )
        config = project.get_config()

        try:
            debezium.add_connector(
                id=project.id,
                type=config["data_source"]["type"],
                config=config,
            )
        except Exception as e:
            project.delete_instance()
            return {"error": f"unable to add project as connector: {e}"}, 400

        try:
            vector_db.create_collection(
                f"turbine_{project.id}", OpenAIModel.embedding_dimension
            )
        except Exception as e:
            project.delete_instance()
            debezium.delete_connector(project.id)
            return {f"error": f"unable to create vector DB: {e}"}, 400

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "add_project",
                    "user": user.id,
                    "project": project.id,
                }
            ),
        )
        logger.info(f"Added project {project.id} for user {user.id}")
        return {"message": f"Project {project.id} added successfully"}, 201

    @requires_auth
    def delete(self, project_id: str):
        project = ProjectModel.get_or_none(
            ProjectModel.id == project_id, ProjectModel.user == get_user()
        )
        if not project:
            return {"error": "Project not found"}, 404

        project.delete_instance()
        debezium.delete_connector(project.id)
        vector_db.drop_collection(f"turbine_{project.id}")

        Log.create(
            user=get_user(),
            info=json.dumps(
                {
                    "action": "remove_project",
                    "user": get_user().id,
                    "project": project.id,
                }
            ),
        )
        logger.info(f"Removed project {project.id} for user {get_user().id}")
        return {
            "message": f"All data purged. Project {project_id} removed successfully. This action can not be reversed."
        }, 200

    @requires_auth
    def put(self, project_id: str):
        user = get_user()

        project = ProjectModel.get_or_none(
            ProjectModel.id == project_id, ProjectModel.user == user
        )
        if not project:
            return {"error": "Project not found or not authorized"}, 404

        args = parser.parse_args()
        if "config" in args:
            project.config = json.dumps(args["config"])

        project.save()

        # @Sumit is this right? can it be optimised
        # disconnect and reconnect debezium
        # re-index vectordb

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "update_project",
                    "user": user.id,
                    "project": project.id,
                }
            ),
        )

        logger.info(f"Updated project {project.id} for user {user.id}")
        return {"message": f"Project {project.id} updated successfully"}, 200
