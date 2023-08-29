from flask_restful import Resource, reqparse
from src.api.auth import requires_auth, get_user
from src.db.models import DataSource as DataSourceModel, Log
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


debezium = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)
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

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "get_data_source",
                    "user": user.id,
                    "data_source": data_source.id,
                }
            ),
        )
        logger.info(f"Retrieved data source {data_source.id} for user {user.id}")
        return data_source.to_dict(), 200

    @requires_auth
    def post(self):
        args = parser.parse_args()
        user = get_user()

        if args["type"] in ["mongo", "postgres"]:
            if not debezium.validate_config(args["type"], args["config"]):
                return {"error": "Invalid configuration"}, 400
        else:
            ...

        data_source = DataSourceModel.create(
            type=args["type"], config=json.dumps(args["config"]), user=user
        )
        config = json.loads(str(data_source.config))

        try:
            if data_source.type in ["mongo", "postgres"]:
                debezium.add_connector(
                    id=data_source.id,
                    type=data_source.type,
                    config=config,
                )
            else:
                ...
        except Exception as e:
            data_source.delete_instance()
            return {"error": str(e)}, 400

        try:
            vector_db.create_collection(
                f"turbine_{data_source.id}", OpenAIModel.embedding_dimension
            )
        except Exception as e:
            data_source.delete_instance()
            debezium.delete_connector(data_source.id)
            return {"error": str(e)}, 400

        Log.create(
            user=user,
            info=json.dumps(
                {
                    "action": "add_data_source",
                    "user": user.id,
                    "data_source": data_source.id,
                }
            ),
        )
        logger.info(f"Added data source {data_source.id} for user {user.id}")
        return {"message": f"Data source {data_source.id} added successfully"}, 201

    @requires_auth
    def delete(self, source_id: str):
        data_source = DataSourceModel.get_or_none(
            DataSourceModel.id == source_id, DataSourceModel.user == get_user()
        )
        if not data_source:
            return {"error": "Data source not found"}, 404

        data_source.delete_instance()
        debezium.delete_connector(data_source.id)
        vector_db.drop_collection(f"turbine_{data_source.id}")

        Log.create(
            user=get_user(),
            info=json.dumps(
                {
                    "action": "remove_data_source",
                    "user": get_user().id,
                    "data_source": data_source.id,
                }
            ),
        )
        logger.info(f"Removed data source {data_source.id} for user {get_user().id}")
        return {"message": f"Data source {source_id} removed successfully"}, 200
