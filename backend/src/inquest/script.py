from src.sources.postgres import Postgres
from src.vectordb.milvus.client import Client
from pymilvus import DataType


class InquestClient:
    def __init__(self, uri, user, password):
        self.client = Client(uri=uri, user=user, password=password)

    def create_collection(self, name, dimension):
        self.client.create_collection(name, params={
            "fields": [
                {"name": "vector", "type": DataType.FLOAT_VECTOR, "params": {
                    "dim": dimension,
                },
                 "indexes": [{"metric_type": "L2"}]}
            ],
            "segment_row_count": 4096,
            "auto_id": True
        })

    def insert_data(self, collection_name, data):
        self.client.insert(collection=collection_name, params={
            "fields": [
                {"name": "vector", "type": DataType.FLOAT_VECTOR, "values": data}
            ]
        })

    def create_index(self, collection_name):
        self.client.create_index(collection=collection_name, field="vector", params={
            "index_type": "IVF_SQ8",
            "metric_type": "L2",
            "params": {"nlist": 2048}
        }, index_name="index1")

    def search(self, collection_name, query_embedding, top_k=10):
        return self.client.search(collection=collection_name, field="vector", data=query_embedding, top_k=top_k,
                                  params={
                                      "metric_type": "L2",
                                      "params": {"nprobe": 10}
                                  })


def get_data_from_postgres(host, database, user, password, table):
    return Postgres.read_table(
        host=host,
        database=database,
        user=user,
        password=password,
        table=table,
    )


def main():
    # Get data from PostgreSQL
    data = get_data_from_postgres("localhost", "postgres", "postgres", "example", "test")

    # Set up Milvus client and perform operations
    client = InquestClient(uri="tcp://localhost:19530", user="root", password="example")
    client.create_collection("collection1", 128)
    client.insert_data("collection1", data)
    client.create_index("collection1")

    query_embedding = []  # Your query embedding here
    results = client.search("collection1", query_embedding)
    print(results)
