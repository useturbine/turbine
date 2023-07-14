from peewee import *

db = SqliteDatabase("database.db")


class User(Model):
    email = CharField(unique=True)
    name = CharField()
    access_token = CharField()
    refresh_token = CharField()

    class Meta:
        database = db


db.create_tables([User])
