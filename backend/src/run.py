import psycopg2
from typing import Optional


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
        for row in cursor:
            print(row)


read_table(
    host="localhost",
    database="postgres",
    user="postgres",
    password="example",
    table="test",
)
