from peewee import *
from datetime import datetime
import json
from config import Config


def create_postgres_connection(connection_string: str):
    """
    Create a Postgres database connection from a connection string.

    Args:
        connection_string (str): A connection string in the format postgres://username:password@host:port/database_name
    """
    parts = connection_string.split("//")[1].split("@")
    credentials, db_info = parts[0], parts[1].split("/")
    username, password = credentials.split(":")
    host, port = db_info[0].split(":")
    database_name = db_info[1]

    return PostgresqlDatabase(
        database=database_name, user=username, password=password, host=host, port=port
    )


db = create_postgres_connection(Config.postgres_url)


class User(Model):
    id = AutoField()
    name = CharField()
    email = CharField(unique=True)
    api_key = CharField(unique=True)

    class Meta:
        database = db


class DataSource(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref="datasources")
    type = CharField()
    config = TextField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "config": json.loads(str(self.config)),
        }


class Log(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref="logs")
    info = TextField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db


class Document(Model):
    id = CharField(primary_key=True)
    created_at = DateTimeField(default=datetime.now())
    data_source = ForeignKeyField(DataSource, backref="documents")
    hash = CharField()

    class Meta:
        database = db


try:
    db.create_tables([User, DataSource, Log, Document])
    User.create(name="Test User", email="test@example.com", api_key="test")
except IntegrityError:
    pass
