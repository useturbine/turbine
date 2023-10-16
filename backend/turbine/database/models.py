from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    UUIDField,
    IntegrityError,
    BooleanField,
)
from playhouse.postgres_ext import BinaryJSONField
from playhouse.pool import PooledPostgresqlExtDatabase
from datetime import datetime
from config import Config
import uuid
from turbine.schema import ExistingPipelineSchema, TaskSchema
from turbine.utils import parse_postgres_url


postgres_params = parse_postgres_url(Config.postgres_url)
db = PooledPostgresqlExtDatabase(
    database=postgres_params.database,
    user=postgres_params.user,
    password=postgres_params.password,
    host=postgres_params.host,
    port=postgres_params.port,
    max_connections=32,
    autoconnect=False,
)


class User(Model):
    id = AutoField()
    external_id = CharField(unique=True, null=True)
    api_key = UUIDField(unique=True, default=uuid.uuid4)
    deleted = BooleanField(default=False)

    class Meta:
        database = db


class Pipeline(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
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
    created_at = DateTimeField(default=datetime.now)
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


with db:
    if db.is_closed():
        db.connect()
    try:
        db.create_tables([User, Task, Pipeline])
        User.create(api_key="b4f9137a-81bc-4acf-ae4e-ee33bef63dec")
    except IntegrityError:
        pass
