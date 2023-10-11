from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    TextField,
    UUIDField,
    IntegrityError,
)
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime
from config import Config
import uuid
from turbine.schema import ExistingIndexSchema


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


class Project(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref="project")
    config = BinaryJSONField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {"id": str(self.id), "config": self.config}


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
    project = ForeignKeyField(Project, backref="documents", on_delete="CASCADE")
    hash = CharField()

    class Meta:
        database = db


class Index(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref="indices")
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    name = CharField()
    description = CharField(null=True)
    vector_db_type = CharField()
    vector_db_config = BinaryJSONField()
    embedding_model_type = CharField()
    embedding_model_config = BinaryJSONField()
    embedding_dimension = CharField()
    similarity_metric = CharField()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def dump(self):
        return ExistingIndexSchema(
            **{
                "id": str(self.id),
                "name": self.name,
                "description": self.description,
                "vector_db": {
                    "type": self.vector_db_type,
                    "config": self.vector_db_config,
                },
                "embedding_model": {
                    "type": self.embedding_model_type,
                    "config": self.embedding_model_config,
                },
                "embedding_dimension": self.embedding_dimension,
                "similarity_metric": self.similarity_metric,
            }
        )

    class Meta:
        database = db


try:
    db.create_tables([User, Project, Log, Document, Index])
    User.create(name="Test User", email="test@example.com", api_key="test")
except IntegrityError:
    pass
