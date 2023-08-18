from vectordb.milvus.client import Client
from model.interface import Model
from datasource.interface import DataSource


class Inquest:
    def __init__(
        self,
        datasource: DataSource,
        model: Model,
        vector_db: Client,
    ) -> None:
        self.datasource = datasource
        self.model = model
        self.vector_db = vector_db

        self.vector_db.drop_collection("test_collection")
        self.vector_db.create_collection(
            name="test_collection",
            dimension=model.embedding_dimension,
            id_max_length=128,
        )
        self.vector_db.create_index(
            collection_name="test_collection",
            params={
                "index_type": "IVF_SQ8",
                "metric_type": "L2",
                "params": {"nlist": 2048},
            },
        )

    def run(self) -> None:
        for pk, doc in self.datasource.get_documents():
            embedding = self.model.get_embedding(doc)
            self.vector_db.insert("test_collection", [[pk], [embedding]])

    def search(self, query: str):
        embedding = self.model.get_embedding(query)
        results = self.vector_db.search(
            "test_collection",
            [embedding],
            10,
            params={"metric_type": "L2", "params": {"nprobe": 10}},
        )
        return results
