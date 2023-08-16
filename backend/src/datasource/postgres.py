import psycopg2
from typing import Optional
from src.datasource.interface import DataSource


class PostgresDataSource(DataSource):
    @staticmethod
    def read_table(
        host: str,
        database: str,
        user: str,
        password: str,
        table: str,
        port: Optional[int] = 5432,
    ):
        conn = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )

        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table};")
            return [row for row in cursor]
