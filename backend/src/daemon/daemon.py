from src.embedding_model.interface import EmbeddingModel
from src.db.models import Log, DataSource as DataSourceModel
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
            collection_name = f"turbine_{update['data_source']}"
            user = DataSourceModel.get_by_id(update["data_source"]).user

            if update["document"]:
                embedding = self.model.get_embedding(update["document"])
                self.vector_db.insert(
                    collection_name,
                    [[update["document_id"]], [embedding]],
                )

                Log.create(
                    user_id=user.id,
                    info={
                        "action": "insert_document",
                        "user": user.id,
                        "data_source": update["data_source"],
                        "document_id": update["document_id"],
                    },
                )
                logger.info(f"Inserted {update['document_id']} into {collection_name}")
                continue

            self.vector_db.delete(
                collection_name,
                update["document_id"],
            )
            Log.create(
                user_id=user.id,
                info={
                    "action": "delete_document",
                    "user": user.id,
                    "data_source": update["data_source"],
                    "document_id": update["document_id"],
                },
            )
            logger.info(f"Deleting {update['document_id']} from {collection_name}")
