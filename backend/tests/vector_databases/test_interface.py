from turbine.vector_databases import VectorItem
from .utils import create_embedding, metadata, create_instance
import pytest


@pytest.mark.parametrize(
    "type",
    [
        "pinecone",
        # "milvus",
    ],
)
class TestVectorDatabase:
    def test_init(self, type: str):
        db = create_instance(type)
        assert db is not None

    def test_validate_config(self, type: str):
        db = create_instance(type)
        db.validate_config()

    def test_insert(self, type: str):
        db = create_instance(type)
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
