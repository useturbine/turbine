from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse
from pydantic import BaseModel


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
        or not parsed_url.username
        or not parsed_url.password
        or not parsed_url.path
        or len(parsed_url.path) < 2
    ):
        raise ValueError("Invalid Postgres connection string")

    return PostgresConnectionParams(
        host=parsed_url.hostname,
        port=parsed_url.port or 5432,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:],
    )
