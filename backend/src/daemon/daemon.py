from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
import json
from src.db.models import DataSource
from typing import Iterator, List


class Daemon:
    def __init__(
        self,
        kafka_url: str,
    ) -> None:
        self.kafka_url = kafka_url

    @staticmethod
    def get_postgres_topics() -> List[str]:
        data_sources = DataSource.select().where(DataSource.type == "postgres")
        topics = []
        for source in data_sources:
            config = json.loads(source.config)
            topics.append(f"inquest.debezium.{source.id}.{config['table']}")
        return topics

    @staticmethod
    def get_mongo_topics() -> List[str]:
        ...

    def get_debezium_messages(self) -> Iterator[ConsumerRecord]:
        topics = [*self.get_postgres_topics()]
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=[self.kafka_url],
            auto_offset_reset="earliest",
        )
        for message in consumer:
            yield message

    def run(self):
        for message in self.get_debezium_messages():
            print(message)
