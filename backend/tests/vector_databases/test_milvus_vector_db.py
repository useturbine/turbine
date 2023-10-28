from ..config import config
from turbine.vector_databases import MilvusVectorDB, VectorItem
from .common import create_embedding, metadata


def create_instance():
    return MilvusVectorDB(
        url=config.milvus_url,
        token=config.milvus_token,
        collection_name="test_collection",
    )


def test_init():
    db = create_instance()
    assert db is not None


def test_validate_config():
    db = create_instance()
    db.validate_config()


def test_insert():
    db = create_instance()
    db.insert(
        [
            VectorItem(
                id="test-id-1",
                vector=create_embedding(),
                metadata=metadata,
            ),
            VectorItem(
                id="test-id-2",
                vector=create_embedding(),
                metadata=metadata,
            ),
        ]
    )
