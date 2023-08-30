from flask_restful import Resource
from flask import request
from src.api.auth import requires_auth, get_user
from src.db.models import DataSource, Log
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
    def get(self, source_id: str):
        query = request.args.get("query")
        if not query:
            return {"error": "Query parameter missing"}, 400
        limit = int(request.args.get("limit", 10))

        user = get_user()
        data_source = DataSource.get_or_none(
            DataSource.id == source_id, DataSource.user == user
        )
        if not data_source:
            return {"error": "Data source not found"}, 404

        query_embedding = embedding_model.get_embedding(query)
        results = vector_db.search(
            collection_name=f"turbine_{data_source.id}",
            data=query_embedding,
            limit=limit,
        )

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "search",
                    "user": user.id,
                    "data_source": data_source.id,
                    "query": query,
                    "limit": limit,
                    "num_results": len(results),
                }
            ),
        )
        logger.info(
            f"User {user.id} searched for {query} in data source {data_source.id} and got {len(results)} results"
        )
        return results, 200
