from pydantic import BaseModel


class PostgresConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str
    table: str


class MongoConfig(BaseModel):
    url: str
    collection: str
