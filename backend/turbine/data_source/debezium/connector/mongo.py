from turbine.data_source.debezium.connector.interface import DebeziumConnector
from turbine.data_source.interface import DataSourceUpdate
from kafka.consumer.fetcher import ConsumerRecord
from typing import List
from turbine.db.models import Project
import json
import logging
import requests
from pymongo import MongoClient
from turbine.schema import MongoConfig

logger = logging.getLogger(__name__)


class MongoConnector(DebeziumConnector):
    def __init__(self, debezium_url: str) -> None:
        self.debezium_url = debezium_url

    @staticmethod
    def validate_config(config: MongoConfig) -> bool:
        try:
            client = MongoClient(host=config.url)
            client.server_info()
        except Exception:
            return False

        try:
            database_name, collection_name = config.collection.split(".")
        except ValueError:
            return False

        database = client[database_name]
        collection_names = database.list_collection_names()

        client.close()
        return collection_name in collection_names

    def add_connector(self, id: str, config: MongoConfig) -> None:
        response = requests.post(
            f"{self.debezium_url}/connectors",
            json={
                "name": f"turbine-{id}",
                "config": {
                    "connector.class": "io.debezium.connector.mongodb.MongoDbConnector",
                    "mongodb.connection.string": config.url,
                    "collection.include.list": config.collection,
                    "topic.prefix": f"turbine.debezium.mongo.{id}",
                },
            },
        )
        response.raise_for_status()
        logger.info(f"Added Mongo connector to Debezium for data source {id}")

    @staticmethod
    def get_topics() -> List[str]:
        projects = Project.select().where(
            Project.config["data_source"]["type"] == "mongo"
        )
        topics = []
        for project in projects:
            topics.append(
                f"turbine.debezium.mongo.{project.id}.{project.config['data_source']['config']['collection']}"
            )
        logger.debug(f"Fetched Mongo topics: {topics}")
        return topics

    @staticmethod
    def parse_message(message: ConsumerRecord) -> DataSourceUpdate:
        project_id = message.topic.split(".")[3]
        project = Project.get_by_id(project_id)
        fields = project.config["data_source"].get("fields", None)
        document_id = json.loads(message.key["payload"]["id"])["$oid"]

        if message.value["payload"]["op"] == "d":
            document = None
        else:
            after_item = json.loads(message.value["payload"]["after"])
            after_item.pop("_id")
            if fields is not None:
                document = "\n".join(
                    f"{k}: {v}" for k, v in after_item.items() if k in fields
                )
            else:
                document = "\n".join(f"{k}: {v}" for k, v in after_item.items())

        return DataSourceUpdate(
            project_id=project_id, document_id=document_id, document=document
        )
