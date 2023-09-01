from flask_restful import Resource
from flask import request
from src.api.auth import requires_auth, get_user
from src.db.models import ProjectModel, Log
from src.vectordb.milvus import MilvusVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config
import json
import logging


logger = logging.getLogger(__name__)

vector_db = MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)
embedding_model = OpenAIModel(api_key=Config.openai_api_key)


class Search(Resource):
    @requires_auth
    def get(self, project_id: str):
        query = request.args.get("query")
        if not query:
            return {"error": "Query parameter missing"}, 400

        limit = int(request.args.get("limit", 10))

        user = get_user()
        project = ProjectModel.get_or_none(
            ProjectModel.id == project_id, ProjectModel.user == user
        )
        if not project:
            return {"error": "Project not found"}, 404

        results = vector_db.search(
            collection_name=f"turbine_{project.id}",
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
        return results, 200
