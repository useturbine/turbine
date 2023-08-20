from peewee import *
from datetime import datetime
import json

db = SqliteDatabase("database.db")


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


db.create_tables([User, DataSource])

try:
    User.create(name="Test User", email="test@example.com", api_key="test")
except IntegrityError:
    pass
