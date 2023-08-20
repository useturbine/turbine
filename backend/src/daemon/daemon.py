from src.embedding_model.interface import EmbeddingModel
from src.vectordb.milvus import MilvusVectorDB
from src.datasource.interface import DataSource


class Daemon:
    def __init__(
        self,
        data_source: DataSource,
        embedding_model: EmbeddingModel,
        vector_db: MilvusVectorDB,
    ) -> None:
        self.data_source = data_source
        self.model = embedding_model
        self.vector_db = vector_db

    def run(self):
        for update in self.data_source.listen_for_updates():
            collection_name = f"inquest_{update['data_source']}"

            if update["document"]:
                print(f"Adding {update['document_id']} to {collection_name}")
                embedding = self.model.get_embedding(update["document"])
                self.vector_db.insert(
                    collection_name,
                    [[update["document_id"]], [embedding]],
                )
                continue

            print(f"Deleting {update['document_id']} from {collection_name}")
            self.vector_db.delete(
                collection_name,
                update["document_id"],
            )
