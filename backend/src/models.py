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


class AWSCost(Model):
    user = ForeignKeyField(User, backref="aws_costs")
    region = CharField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    service = CharField()
    operation = CharField()
    cost = FloatField()

    class Meta:
        database = db
        indexes = (
            # Create a unique constraint on the following columns
            (
                ("user", "region", "start_time", "end_time", "service", "operation"),
                True,
            ),
        )


db.create_tables([User, AWSCost])
