from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    UUIDField,
    IntegrityError,
    BooleanField,
)
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime
from config import Config
import uuid
from turbine.schema import ExistingPipelineSchema, TaskSchema
import uuid


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
    external_id = CharField(unique=True, null=True)
    api_key = UUIDField(unique=True, default=uuid.uuid4)
    deleted = BooleanField(default=False)

    class Meta:
        database = db


class Pipeline(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    name = CharField()
    description = CharField(null=True)
    user = ForeignKeyField(User, backref="pipelines")
    data_source = BinaryJSONField()
    embedding_model = BinaryJSONField()
    vector_database = BinaryJSONField()
    deleted = BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        database = db

    def dump(self):
        return ExistingPipelineSchema(
            **{
                "id": str(self.id),
                "name": self.name,
                "description": self.description,
                "data_source": self.data_source,
                "embedding_model": self.embedding_model,
                "vector_database": self.vector_database,
            }
        )


class Task(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    pipeline = ForeignKeyField(Pipeline, backref="tasks")
    type = CharField()
    metadata = BinaryJSONField(null=True)
    created_at = DateTimeField(default=datetime.now())
    finished_at = DateTimeField(null=True)
    successful = BooleanField(default=False)

    def dump(self):
        return TaskSchema(
            **{
                "id": self.id,
                "pipeline": self.pipeline.id,
                "type": self.type,
                "metadata": self.metadata,
                "created_at": self.created_at,
                "finished_at": self.finished_at,
                "successful": self.successful,
            }
        )

    class Meta:
        database = db


try:
    db.create_tables([User, Task, Pipeline])
    User.create(api_key="b4f9137a-81bc-4acf-ae4e-ee33bef63dec")
except IntegrityError:
    pass
