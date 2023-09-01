import requests
from typing import List, Iterator, Tuple, Optional
from datetime import datetime
from kafka import KafkaConsumer
import json
from src.datasource.interface import DataSource as DataSourceInterface, DataSourceUpdate
import logging
from src.datasource.debezium.connector.postgres import PostgresConnector
from src.datasource.debezium.connector.mongo import MongoConnector


logger = logging.getLogger(__name__)


class DebeziumDataSource(DataSourceInterface):
    def __init__(
        self,
        debezium_url: str,
        kafka_url: str,
        refresh_topics_ms: int = 1000,
    ) -> None:
        self.consumer = KafkaConsumer(
            bootstrap_servers=[kafka_url],
            auto_offset_reset="earliest",
            key_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
            consumer_timeout_ms=refresh_topics_ms,
        )
        self.debezium_url = debezium_url
        logger.debug(
            f"Initialized Debezium data source with {debezium_url} and {kafka_url}"
        )
        self.postgres_connector = PostgresConnector(debezium_url)
        self.mongo_connector = MongoConnector(debezium_url)

    def validate_config(self, type: str, config) -> bool:
        if type == "mongo":
            return self.mongo_connector.validate_config(config)
        elif type == "postgres":
            return self.postgres_connector.validate_config(config)
        return False

    def add_connector(
        self,
        id: str,
        type: str,
        config,
    ) -> None:
        if type == "mongo":
            self.mongo_connector.add_connector(id=id, config=config)
        elif type == "postgres":
            self.postgres_connector.add_connector(id=id, config=config)
        else:
            raise Exception("Unknown connector type")

    def delete_connector(self, id: str) -> None:
        connector_name = f"turbine-{id}"
        response = requests.delete(f"{self.debezium_url}/connectors/{connector_name}")
        response.raise_for_status()
        logger.info(f"Removed connector {connector_name} from Debezium")

    def get_topics(self) -> List[str]:
        return [
            *self.postgres_connector.get_topics(),
            *self.mongo_connector.get_topics(),
        ]

    def listen_for_updates(self) -> Iterator[DataSourceUpdate]:
        past_topics = []

        while True:
            topics = self.get_topics()
            if topics and topics != past_topics:
                logger.info(f"Subscribing to {topics}")
                self.consumer.subscribe(topics)
                past_topics = topics

            for message in self.consumer:
                if message.value:
                    if message.topic.startswith("turbine.debezium.postgres"):
                        yield self.postgres_connector.parse_message(message)
                    elif message.topic.startswith("turbine.debezium.mongo"):
                        yield self.mongo_connector.parse_message(message)
                    else:
                        raise Exception("Unknown topic")

    def get_documents(
        self, updated_since: Optional[datetime] = None
    ) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError
