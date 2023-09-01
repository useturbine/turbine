from src.datasource.debezium.connector.interface import DebeziumConnector
from src.datasource.interface import DataSourceUpdate
from kafka.consumer.fetcher import ConsumerRecord
from typing import List
from src.db.models import Project
import json
import logging
import requests
import psycopg2
from src.schema import PostgresConfig

logger = logging.getLogger(__name__)


class PostgresConnector(DebeziumConnector):
    def __init__(self, debezium_url: str) -> None:
        self.debezium_url = debezium_url

    def add_connector(self, id: str, config: PostgresConfig) -> None:
        response = requests.post(
            f"{self.debezium_url}/connectors",
            json={
                "name": f"turbine-{id}",
                "config": {
                    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
                    "plugin.name": "pgoutput",
                    "publication.autocreate.mode": "filtered",
                    "include.schema.changes": "false",
                    "database.hostname": config.host,
                    "database.port": config.port,
                    "database.user": config.user,
                    "database.password": config.password,
                    "database.dbname": config.database,
                    "table.include.list": config.table,
                    "topic.prefix": f"turbine.debezium.postgres.{id}",
                },
            },
        )
        response.raise_for_status()
        logger.info(f"Added Postgres connector to Debezium for data source {id}")

    @staticmethod
    def parse_message(message: ConsumerRecord) -> DataSourceUpdate:
        data_source = message.topic.split(".")[3]
        document_id = str(message.key["payload"]["id"])

        document = None
        if message.value["payload"]["op"] != "d":
            document = "\n".join(
                f"{k}: {v}" for k, v in message.value["payload"]["after"].items()
            )

        return {
            "data_source": data_source,
            "document_id": document_id,
            "document": document,
        }

    @staticmethod
    def get_topics() -> List[str]:
        projects = Project.select().where(
            Project.config["data_source"]["type"] == "postgres"
        )
        topics = []
        for project in projects:
            topics.append(
                f"turbine.debezium.postgres.{project.id}.{project.config['data_source']['config']['table']}"
            )
        logger.debug(f"Fetched Postgres topics: {topics}")
        return topics

    @staticmethod
    def validate_config(config: PostgresConfig) -> bool:
        try:
            connection = psycopg2.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                dbname=config.database,
            )
        except psycopg2.OperationalError:
            return False

        try:
            schema_name, table_name = config.table.split(".")
        except ValueError:
            return False

        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
            )
            """,
            [schema_name, table_name],
        )
        table_exists = cursor.fetchone()

        cursor.close()
        connection.close()

        if table_exists is not None and table_exists[0]:
            return True
        return False
