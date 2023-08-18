from src.datasource.interface import DataSource

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, RealDictRow
from typing import (Optional, Iterator, Tuple)
from datetime import datetime
from pgoutput import get_changes, Message


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

    def listen_for_updates_with_trigger(self) -> Iterator[Tuple[str, str]]:
        """
        by NOTIFY/LISTEN trigger

// write something like this
CREATE OR REPLACE FUNCTION notify_insert() RETURNS trigger AS $$
BEGIN
    NOTIFY new_inserts;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notify_insert
AFTER INSERT ON your_table_name
FOR EACH ROW EXECUTE FUNCTION notify_insert();


        """
        with self.connection.cursor() as cursor:
            cursor.execute("LISTEN new_inserts;")

            while True:
                # Waiting for a notification
                self.connection.poll()
                if not self.connection.notifies:
                    continue

                self.connection.notifies.pop()

                # Fetching the new rows
                # Assuming that rows have a timestamp column to filter the new rows
                # Adjust the logic if there's a better way to identify "new" rows
                if self.updated_at_column:
                    now = datetime.now()
                    query = sql.SQL("SELECT * FROM {} WHERE {} > %s").format(
                        self.table,
                        sql.Identifier(self.updated_at_column)
                    )
                    cursor.execute(query, (now,))
                    for row in cursor:
                        yield self.format_row(row)

    def listen_for_updates_with_WAL(self, db, user, password, host, port) -> Iterator[Tuple[str, str]]:
        """
Configure your PostgreSQL for Logical Replication:

1. configure in `postgresql.conf`:
```
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

2. Restart PostgreSQL after making these changes.

3.
Set up a Publication on the master database:
`CREATE PUBLICATION my_publication FOR TABLE your_table_name;`
"""
        # replication connection
        repl_conn = psycopg2.connect(
            dbname=db,
            user=user,
            password=password,
            host=host,
            port=port,
            connection_factory=psycopg2.extras.LogicalReplicationConnection
        )

        # create a replication slot if not exists
        try:
            with repl_conn.cursor() as cur:
                cur.create_replication_slot(slot_name="my_slot", output_plugin="pgoutput")
        except Exception as e:
            # slot already exists
            pass

        # Start replicating using the slot
        with repl_conn.cursor() as cur:
            cur.start_replication(slot_name="my_slot",
                                  options={'proto_version': 1, 'publication_names': 'my_publication'})

            for msg in cur:
                changes = get_changes(msg.payload)
                for change in changes:
                    if isinstance(change, Message.Insert):
                        data = change.data
                        # dict of new data
                        yield self.format_row(data)

                    elif isinstance(change, Message.Delete):
                        data = change.data
                        # need to remove index for this in vectorDB
                        yield self.format_row(data)

                    elif isinstance(change, Message.Update):
                        data = change.data
                        old_data = change.old_data

                        # remove index of old_data
                        # add index for data

                        yield self.format_row(data)

