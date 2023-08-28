from src.datasource.debezium.connector.interface import DebeziumConnector
from src.datasource.interface import DataSourceUpdate
from kafka.consumer.fetcher import ConsumerRecord
from typing import List
from src.db.models import DataSource
import json
import logging
import requests
from pymongo import MongoClient

logger = logging.getLogger(__name__)


class MongoConnector(DebeziumConnector):
    def __init__(self, debezium_url: str) -> None:
        self.debezium_url = debezium_url

    @staticmethod
    def validate_config(config: dict) -> bool:
        if "url" not in config or "collection" not in config:
            return False

        try:
            client = MongoClient(host=config["url"])
            client.server_info()
        except Exception:
            return False

        try:
            database_name, collection_name = config["collection"].split(".")
        except ValueError:
            return False

        database = client[database_name]
        collection_names = database.list_collection_names()

        client.close()
        return collection_name in collection_names

    def add_connector(self, id: str, config: dict) -> None:
        response = requests.post(
            f"{self.debezium_url}/connectors",
            json={
                "name": f"turbine-{id}",
                "config": {
                    "connector.class": "io.debezium.connector.mongodb.MongoDbConnector",
                    "mongodb.connection.string": config["url"],
                    "collection.include.list": config["collection"],
                    "topic.prefix": f"turbine.debezium.mongo.{id}",
                },
            },
        )
        response.raise_for_status()
        logger.info(f"Added Mongo connector to Debezium for data source {id}")

    @staticmethod
    def get_topics() -> List[str]:
        data_sources = DataSource.select().where(DataSource.type == "mongo")
        topics = []
        for source in data_sources:
            config = json.loads(source.config)
            topics.append(f"turbine.debezium.mongo.{source.id}.{config['collection']}")
        logger.debug(f"Fetched Mongo topics: {topics}")
        return topics

    @staticmethod
    def parse_message(message: ConsumerRecord) -> DataSourceUpdate:
        data_source = message.topic.split(".")[3]
        document_id = json.loads(message.key["payload"]["id"])["$oid"]

        if message.value["payload"]["op"] == "d":
            document = None
        else:
            after_item = json.loads(message.value["payload"]["after"])
            after_item.pop("_id")
            document = "\n".join(f"{k}: {v}" for k, v in after_item.items())

        return {
            "data_source": data_source,
            "document_id": document_id,
            "document": document,
        }
