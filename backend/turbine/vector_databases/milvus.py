from turbine.vector_databases import VectorDatabase, VectorItem, VectorSearchResult
from pydantic import BaseModel
from typing import Literal
from pymilvus import Collection, connections
from pymilvus.exceptions import SchemaNotReadyException, MilvusException
import uuid
from wrapt_timeout_decorator.wrapt_timeout_decorator import timeout


class MilvusVectorDB(VectorDatabase, BaseModel):
    type: Literal["milvus"] = "milvus"
    url: str
    token: str
    collection_name: str
    batch_size: int = 128
    _connection_alias: str

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._connection_alias = uuid.uuid4().hex

    @timeout(11)
    def connect(self) -> None:
        if not connections.has_connection(self._connection_alias):
            connections.connect(self._connection_alias, uri=self.url, token=self.token)

    def validate_config(self) -> None:
        try:
            self.connect()
        except MilvusException as e:
            if "Timeout" in str(e):
                raise ValueError("Invalid Milvus URL")
            elif "timed out" in str(e):
                raise ValueError("Invalid Milvus token")
            else:
                raise e
        try:
            Collection(self.collection_name, using=self._connection_alias)
        except SchemaNotReadyException:
            raise ValueError("Invalid Milvus collection name")

    def insert(self, data: list[VectorItem]) -> None:
        self.connect()
        collection = Collection(self.collection_name, using=self._connection_alias)
        collection.insert(data=[item.model_dump() for item in data])
        collection.flush()

    def search(self, data: list[float], limit: int) -> list[VectorSearchResult]:
        self.connect()
        collection = Collection(self.collection_name, using=self._connection_alias)
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
        self.connect()
        collection = Collection(self.collection_name, using=self._connection_alias)
        collection.delete(f"id = {id}")
        collection.flush()

    @property
    def embedding_dimension(self) -> int:
        self.connect()
        collection = Collection(self.collection_name, using=self._connection_alias)
        description = collection.describe()
        embedding_field = list(
            filter(lambda field: field["name"] == "embedding", description["fields"])
        )[0]
        return embedding_field["params"]["dim"]
