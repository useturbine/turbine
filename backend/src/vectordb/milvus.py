from pymilvus import Collection
from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from typing import List, Optional
from src.vectordb.interface import VectorDB, VectorItem, VectorSearchResult


class MilvusVectorDB(VectorDB):
    def __init__(self, url: str, id_max_length: Optional[int] = 512) -> None:
        connections.connect("default", uri=url)
        self.id_max_length = id_max_length

    def create_collection(self, name: str, dimension: int) -> None:
        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.VARCHAR,
                is_primary=True,
                auto_id=False,
                max_length=self.id_max_length,
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

    @staticmethod
    def insert(collection_name: str, data: List[VectorItem]) -> None:
        collection = Collection(collection_name)
        collection.insert(
            data=[[item["id"] for item in data], [item["vector"] for item in data]]
        )
        collection.flush()

    @staticmethod
    def search(
        collection_name: str, data: List[float], limit: int
    ) -> List[VectorSearchResult]:
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
        return [
            {
                "id": result.id,
                "distance": result.distance,
            }
            for result in list(results)[0]  # type: ignore
        ]

    @staticmethod
    def delete(collection_name: str, id: str) -> None:
        collection = Collection(collection_name)
        collection.delete(f"id = {id}")
        collection.flush()

    @staticmethod
    def drop_collection(collection_name: str) -> None:
        utility.drop_collection(collection_name)
