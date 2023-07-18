from peewee import *

db = SqliteDatabase("database.db")


class User(Model):
    email = CharField(unique=True)
    name = CharField(null=True)
    aws_access_key = CharField(null=True)
    aws_secret_key = CharField(null=True)
    aws_terraform = CharField(null=True)

    class Meta:
        database = db


db.create_tables([User])
