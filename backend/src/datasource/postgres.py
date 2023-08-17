import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, RealDictRow
from typing import Optional, Iterator, Tuple
from datasource.interface import DataSource


class PostgresDataSource(DataSource):
    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        table: str,
        primary_key: str = "id",
        port: Optional[int] = 5432,
    ) -> None:
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            cursor_factory=RealDictCursor,
        )
        self.table = sql.Identifier(table)
        self.primary_key = primary_key

    @staticmethod
    def format_row(row: RealDictRow) -> str:
        """Format a RealDictRow to a string where each key-value pair is on a new line."""
        return "\n".join(f"{k}: {v}" for k, v in row.items())

    def get_all_documents(self) -> Iterator[Tuple[str, str]]:
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(self.table))
            row: RealDictRow
            for row in cursor:  # type: ignore
                yield (row[self.primary_key], self.format_row(row))
