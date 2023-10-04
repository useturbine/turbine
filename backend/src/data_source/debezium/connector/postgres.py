from src.data_source.debezium.connector.interface import DebeziumConnector
from src.data_source.interface import DataSourceUpdate
from kafka.consumer.fetcher import ConsumerRecord
from typing import List
from src.db.models import Project
import logging
import requests
import psycopg2
from pydantic import BaseModel
from urllib.parse import urlparse
from src.schema import PostgresConfig

logger = logging.getLogger(__name__)


class PostgresConnectionParams(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str


def parse_postgres_url(url: str) -> PostgresConnectionParams:
    """
    Parse Postgres connection params from a connection string URL.

    Args:
        url (str): A connection string in the format postgres://username:password@host:port/database_name
    """
    parsed_url = urlparse(url)
    if (
        parsed_url.scheme != "postgres"
        or not parsed_url.hostname
        or not parsed_url.port
        or not parsed_url.username
        or not parsed_url.password
        or not parsed_url.path
        or len(parsed_url.path) < 2
    ):
        raise ValueError("Invalid Postgres connection string")

    return PostgresConnectionParams(
        host=parsed_url.hostname,
        port=parsed_url.port,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:],
    )


class PostgresConnector(DebeziumConnector):
    def __init__(self, debezium_url: str) -> None:
        self.debezium_url = debezium_url

    def add_connector(self, id: str, config: PostgresConfig) -> None:
        connection_params = parse_postgres_url(config.url)
        response = requests.post(
            f"{self.debezium_url}/connectors",
            json={
                "name": f"turbine-{id}",
                "config": {
                    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
                    "plugin.name": "pgoutput",
                    "publication.autocreate.mode": "filtered",
                    "include.schema.changes": "false",
                    "database.hostname": connection_params.host,
                    "database.port": connection_params.port,
                    "database.user": connection_params.user,
                    "database.password": connection_params.password,
                    "database.dbname": connection_params.database,
                    "table.include.list": config.table,
                    "topic.prefix": f"turbine.debezium.postgres.{id}",
                },
            },
        )
        response.raise_for_status()
        logger.info(f"Added Postgres connector to Debezium for data source {id}")

    @staticmethod
    def parse_message(message: ConsumerRecord) -> DataSourceUpdate:
        project_id = message.topic.split(".")[3]
        project = Project.get_by_id(project_id)
        fields = project.config["data_source"].get("fields", None)

        document_id = str(message.key["payload"]["id"])

        document = None
        if message.value["payload"]["op"] != "d":
            if fields is not None:
                document = "\n".join(
                    f"{k}: {v}"
                    for k, v in message.value["payload"]["after"].items()
                    if k in fields
                )
            else:
                document = "\n".join(
                    f"{k}: {v}" for k, v in message.value["payload"]["after"].items()
                )

        return DataSourceUpdate(
            project_id=project_id,
            document_id=document_id,
            document=document,
        )

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
        connection_params = parse_postgres_url(config.url)
        try:
            connection = psycopg2.connect(
                host=connection_params.host,
                port=connection_params.port,
                user=connection_params.user,
                password=connection_params.password,
                dbname=connection_params.database,
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
