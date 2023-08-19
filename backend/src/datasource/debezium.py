import requests


class Debezium:
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url = url

    def add_postgres_connector(
        self,
        id: int,
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
                "name": f"inquest-{id}",
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
                    "topic.prefix": f"inquest.debezium.{id}",
                },
            },
        )
        response.raise_for_status()
