from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
import json
from src.db.models import DataSource
from src.embedding_model.interface import EmbeddingModel
from src.vectordb.milvus import MilvusVectorDB
from typing import Iterator, List, TypedDict, Optional


class ParsedMessage(TypedDict):
    data_source: str
    document_id: str
    document: Optional[str]


class Daemon:
    def __init__(
        self, kafka_url: str, embedding_model: EmbeddingModel, vector_db: MilvusVectorDB
    ) -> None:
        self.kafka_url = kafka_url
        self.model = embedding_model
        self.vector_db = vector_db

    @staticmethod
    def get_postgres_topics() -> List[str]:
        data_sources = DataSource.select().where(DataSource.type == "postgres")
        topics = []
        for source in data_sources:
            config = json.loads(source.config)
            topics.append(f"inquest.debezium.{source.id}.{config['table']}")
        return topics

    def parse_postgres_message(self, message: ConsumerRecord) -> ParsedMessage:
        data_source = message.topic.split(".")[2]
        document_id = message.key["payload"]["id"]
        if message.value["payload"]["op"] == "d":
            document = None
        else:
            row_dict = message.value["payload"]["after"]
            document = "\n".join(f"{k}: {v}" for k, v in row_dict.items())
        return {
            "data_source": data_source,
            "document_id": str(document_id),
            "document": document,
        }

    @staticmethod
    def get_mongo_topics() -> List[str]:
        ...

    def get_debezium_messages(self) -> Iterator[ConsumerRecord]:
        topics = [*self.get_postgres_topics()]
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=[self.kafka_url],
            auto_offset_reset="earliest",
            key_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None,
        )
        for message in consumer:
            if message.value:
                yield message

    def run(self):
        for message in self.get_debezium_messages():
            parsed_message = self.parse_postgres_message(message)
            collection_name = f"inquest_{parsed_message['data_source']}"

            if parsed_message["document"]:
                embedding = self.model.get_embedding(parsed_message["document"])
                self.vector_db.insert(
                    collection_name,
                    [[parsed_message["document_id"]], [embedding]],
                )
            else:
                self.vector_db.delete(
                    collection_name,
                    parsed_message["document_id"],
                )
