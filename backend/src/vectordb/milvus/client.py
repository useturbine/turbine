from pymilvus import Collection
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from typing import Dict, Literal, List


class Client:
    def __init__(self, host: str, port: int, user: str, password: str):
        connections.connect(
            "default", host=host, port=port, user=user, password=password
        )

    @staticmethod
    def create_collection(name: str, dimension: int):
        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.VARCHAR,
                is_primary=True,
                auto_id=False,
                max_length=128,
            ),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        ]
        schema = CollectionSchema(fields)
        return Collection(name, schema)

    @staticmethod
    def create_index(collection_name: str, params: Dict):
        Collection(collection_name).create_index(
            field_name="embedding", index_params=params
        )

    @staticmethod
    def insert(collection_name: str, data: List[List]):
        collection = Collection(collection_name)
        collection.insert(data=data)
        collection.flush()

    @staticmethod
    def search(collection_name: str, data: List, limit: int, params: Dict):
        collection = Collection(collection_name)
        collection.load()
        results = collection.search(
            data=data, anns_field="embedding", limit=limit, param=params
        )
        collection.release()
        return results

    @staticmethod
    def drop_collection(collection_name: str):
        utility.drop_collection(collection_name)
