from peewee import *
from datetime import datetime
import json
import jsonschema
import os
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


class ProjectModel(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref="project")
    config = TextField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db

    def get_config(self):
        return json.loads(str(self.config))

    def save(self, *args, **kwargs):
        self.validate_config()
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "config": self.get_config(),
        }

    def validate_config(self):
        schema = {
            "type": "object",
            "properties": {
                "data_source": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["mongo", "postgres"]},
                    },
                    "required": ["type"],
                },
                "embedding": {
                    "type": "object",
                    "properties": {
                        "dimensions": {"type": "integer"},
                        "chunk_size": {"type": "integer"},
                    },
                    "required": [],
                },
                "vectordb": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string"},
                        "port": {"type": "integer"},
                    },
                    "required": ["host", "port"],
                },
            },
            "required": ["data_source"],
        }

        try:
            jsonschema.validate(instance=self.get_config(), schema=schema)
        except (ValueError, jsonschema.ValidationError) as e:
            raise ValueError(f"Invalid config: {str(e)}")


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
    project = ForeignKeyField(ProjectModel, backref="documents")
    hash = CharField()

    class Meta:
        database = db


try:
    db.create_tables([User, ProjectModel, Log, Document])
    User.create(name="Test User", email="test@example.com", api_key="test")
except IntegrityError:
    pass
