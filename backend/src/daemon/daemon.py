from src.embedding_model.interface import EmbeddingModel
from src.vectordb.milvus import MilvusVectorDB
from src.datasource.interface import DataSource
import logging

logger = logging.getLogger(__name__)


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
            logger.info(f"Received update: {update}")
            collection_name = f"inquest_{update['data_source']}"

            if update["document"]:
                logger.info(f"Inserting {update['document_id']} into {collection_name}")
                embedding = self.model.get_embedding(update["document"])
                self.vector_db.insert(
                    collection_name,
                    [[update["document_id"]], [embedding]],
                )
                continue

            logger.info(f"Deleting {update['document_id']} from {collection_name}")
            self.vector_db.delete(
                collection_name,
                update["document_id"],
            )
