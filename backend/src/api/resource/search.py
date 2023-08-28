from flask_restful import Resource
from flask import request
from src.api.auth import requires_auth, get_user
from src.db.models import DataSource
from src.vectordb.milvus import MilvusVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config


vector_db = MilvusVectorDB(url=Config.milvus_url)
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
        hits = vector_db.search(
            collection_name=f"turbine_{data_source.id}",
            data=query_embedding,
            limit=limit,
        )
        results = [
            {
                "id": result.id,
                "distance": result.distance,
            }
            for result in list(hits)[0]  # type: ignore
        ]
        return results, 200
