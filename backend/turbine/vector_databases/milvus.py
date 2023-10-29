from pymilvus import Collection
from pymilvus import connections, Collection
from turbine.vector_databases import VectorDatabase, VectorItem, VectorSearchResult
from pydantic import BaseModel
from typing import Literal


class MilvusVectorDB(VectorDatabase, BaseModel):
    type: Literal["milvus"] = "milvus"
    url: str
    token: str
    collection_name: str
    batch_size: int = 128

    def __init__(self, **data) -> None:
        super().__init__(**data)
        connections.connect("default", uri=self.url, token=self.token)

    def insert(self, data: list[VectorItem]) -> None:
        collection = Collection(self.collection_name)
        collection.insert(data=[item.model_dump() for item in data])
        collection.flush()

    def search(self, data: list[float], limit: int) -> list[VectorSearchResult]:
        collection = Collection(self.collection_name)
        collection.load()
        metric_type = collection.index().params["metric_type"]
        results = collection.search(
            data=[data],
            anns_field="embedding",
            limit=limit,
            param={"metric_type": metric_type},
        )
        collection.release()
        return [
            VectorSearchResult(id=result.id, score=result.distance, metadata={})
            for result in list(results)[0]  # type: ignore
        ]

    def delete(self, id: str) -> None:
        collection = Collection(self.collection_name)
        collection.delete(f"id = {id}")
        collection.flush()
