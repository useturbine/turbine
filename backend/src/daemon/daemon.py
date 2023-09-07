from src.db.models import Log, Project, Document
from src.vector_db import VectorItem
from src.data_source import DebeziumDataSource
import logging
import hashlib
from src.utils import get_vector_db
from src.embedding_model import get_embedding_model
from config import Config


logger = logging.getLogger(__name__)

data_source = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)


class Daemon:
    @staticmethod
    def run():
        for update in data_source.listen_for_updates():
            logger.info(f"Received update: {update}")
            collection_name = f"turbine{update.project_id}"

            project = Project.get_by_id(update.project_id)
            user = project.user
            vector_db = get_vector_db(project.config["vector_db"])
            model = get_embedding_model(project.config["embedding_model"])

            if not update.document:
                vector_db.delete(
                    collection_name,
                    update.document_id,
                )
                Log.create(
                    user_id=user.id,
                    info={
                        "action": "delete_document",
                        "user": user.id,
                        "project": update.project_id,
                        "document": update.document_id,
                    },
                )
                logger.info(f"Deleting {update.document_id} from {collection_name}")
                continue

            document = Document.get_or_none(
                Document.id == update.document_id,
                Document.project == update.project_id,
            )
            document_hash = hashlib.sha256(update.document.encode("utf-8")).hexdigest()
            if document and document.hash == document_hash:
                logger.info(f"Skipping {update.document_id}")
                continue

            embedding = model.model.get_embedding(update.document)
            print(collection_name)
            vector_db.insert(
                collection_name,
                [VectorItem(id=update.document_id, vector=embedding)],
            )

            if document:
                document.hash = document_hash
                document.save()
            else:
                Document.create(
                    id=update.document_id,
                    project=update.project_id,
                    hash=document_hash,
                )

            Log.create(
                user_id=user.id,
                info={
                    "action": "insert_document",
                    "user": user.id,
                    "project": update.project_id,
                    "document_id": update.document_id,
                },
            )
            logger.info(f"Inserted {update.document_id} into {collection_name}")
