from pymilvus import Collection
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from typing import List


class MilvusVectorDB:
    def __init__(self, url: str) -> None:
        connections.connect("default", uri=url)

    @staticmethod
    def create_collection(name: str, id_max_length: int, dimension: int) -> Collection:
        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.VARCHAR,
                is_primary=True,
                auto_id=False,
                max_length=id_max_length,
            ),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        ]
        schema = CollectionSchema(fields)
        collection = Collection(name, schema)
        collection.create_index(
            field_name="embedding",
            index_params={
                "index_type": "IVF_SQ8",
                "metric_type": "L2",
                "params": {"nlist": 2048},
            },
        )
        return collection

    @staticmethod
    def insert(collection_name: str, data: List) -> None:
        collection = Collection(collection_name)
        collection.insert(data=data)
        collection.flush()

    @staticmethod
    def search(collection_name: str, data: List[float], limit: int):
        collection = Collection(collection_name)
        collection.load()
        results = collection.search(
            data=[data],
            anns_field="embedding",
            limit=limit,
            param={
                "metric_type": "L2",
            },
        )
        collection.release()
        return results

    @staticmethod
    def delete(collection_name: str, id: str):
        collection = Collection(collection_name)
        collection.delete(f"id = {id}")
        collection.flush()

    @staticmethod
    def drop_collection(collection_name: str):
        utility.drop_collection(collection_name)
