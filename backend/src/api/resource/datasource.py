from flask_restful import Resource, reqparse
from src.api.auth import requires_auth, get_user
from src.db.models import DataSource as DataSourceModel
from typing import Optional
from src.datasource.debezium import Debezium
from src.vectordb.milvus import MilvusVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config
import json

parser = reqparse.RequestParser()
parser.add_argument(
    "type",
    type=str,
    required=True,
    choices=["mongo", "postgres"],
    help="Data source type must be either mongo or postgres",
)
parser.add_argument(
    "config",
    type=dict,
    required=True,
    help="Configuration details for the data source cannot be blank",
)


debezium = Debezium(debezium_url=Config.debezium_url, kafka_url=Config.kafka_url)
vector_db = MilvusVectorDB(url=Config.milvus_url)


class DataSource(Resource):
    @requires_auth
    def get(self, source_id: Optional[str] = None):
        user = get_user()
        if not source_id:
            data_sources = [
                source.to_dict()
                for source in DataSourceModel.select().where(
                    DataSourceModel.user == user
                )
            ]
            return data_sources, 200

        data_source = DataSourceModel.get_or_none(
            DataSourceModel.id == source_id, DataSourceModel.user == user
        )
        if not data_source:
            return {"error": "Data source not found"}, 404
        return data_source.to_dict(), 200

    @requires_auth
    def post(self):
        args = parser.parse_args()
        data_source = DataSourceModel.create(
            type=args["type"], config=json.dumps(args["config"]), user=get_user()
        )
        config = json.loads(str(data_source.config))

        if data_source.type == "mongo":
            debezium.add_mongo_connector(
                id=data_source.id,
                url=config["url"],
                collection=config["collection"],
            )
        elif data_source.type == "postgres":
            debezium.add_postgres_connector(
                id=data_source.id,
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                table=config["table"],
            )

        vector_db.create_collection(
            f"inquest_{data_source.id}", 512, OpenAIModel.embedding_dimension
        )

        return {"message": f"Data source {data_source.id} created successfully"}, 201

    @requires_auth
    def delete(self, source_id: str):
        data_source = DataSourceModel.get_or_none(
            DataSourceModel.id == source_id, DataSourceModel.user == get_user()
        )
        if data_source:
            data_source.delete_instance()
            return {"message": f"Data source {source_id} removed successfully"}, 200
        return {"error": "Data source not found"}, 404
