import requests
from kafka import KafkaConsumer
import json


class Debezium:
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url = url

    def add_postgres_connector(
        self,
        name: str,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        table: str,
    ) -> None:
        response = requests.post(
            f"{self.url}/connectors",
            json={
                "name": name,
                "config": {
                    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
                    "plugin.name": "pgoutput",
                    "publication.autocreate.mode": "filtered",
                    "include.schema.changes": "false",
                    "database.hostname": host,
                    "database.port": port,
                    "database.user": user,
                    "database.password": password,
                    "database.dbname": database,
                    "table.include.list": table,
                    "topic.prefix": f"debezium.postgres.{name}",
                },
            },
        )
        response.raise_for_status()
        return response.json()


class Kafka:
    def __init__(
        self,
        server: str,
        consumer_id: str,
    ) -> None:
        self.server = server
        # self.consumer_id = consumer_id

    def get_postgres_updates(self, connector: str, table: str):
        print(f"debezium.postgres.{connector}.{table}")
        consumer = KafkaConsumer(
            f"debezium.postgres.{connector}.{table}",
            bootstrap_servers=[self.server],
            # group_id=self.consumer_id,
            auto_offset_reset="earliest",
            # enable_auto_commit=True,
            key_deserializer=lambda x: json.loads(x.decode("utf-8")),
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        for message in consumer:
            print(message.value["payload"])
