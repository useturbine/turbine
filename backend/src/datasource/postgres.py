import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, RealDictRow
from typing import Optional, Iterator, Tuple
from datasource.interface import DataSource
from datetime import datetime


class PostgresDataSource(DataSource):
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        table: str,
        pk_column: str,
        updated_at_column: Optional[str] = None,
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
        self.pk_column = pk_column
        self.updated_at_column = updated_at_column

    def format_row(self, row: RealDictRow) -> Tuple[str, str]:
        return (
            str(row[self.pk_column]),
            "\n".join(f"{k}: {v}" for k, v in row.items()),
        )

    def get_documents(
        self, updated_since: Optional[datetime] = None
    ) -> Iterator[Tuple[str, str]]:
        with self.connection.cursor() as cursor:
            if updated_since:
                if not self.updated_at_column:
                    raise Exception(
                        "updated_at_column must be provided if using updated_since"
                    )
                query = sql.SQL("SELECT * FROM {} WHERE updated_at > %s").format(
                    self.table
                )
                cursor.execute(query, (updated_since,))
            else:
                cursor.execute(sql.SQL("SELECT * FROM {}").format(self.table))

            row: RealDictRow
            for row in cursor:  # type: ignore
                yield self.format_row(row)

    def listen_for_updates(self) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError(
            "PostgresDataSource.listen_for_updates is not implemented"
        )
