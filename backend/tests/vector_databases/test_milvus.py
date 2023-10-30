import pytest
from tests.config import config
from turbine.vector_databases import MilvusVectorDB


def test_validate_config_invalid_url():
    db = MilvusVectorDB(
        url="http://localhost:1234",
        token=config.milvus_token,
        collection_name="test_collection",
    )
    with pytest.raises(ValueError, match="Invalid Milvus URL"):
        db.validate_config()


def test_validate_config_invalid_token():
    db = MilvusVectorDB(
        url=config.milvus_url,
        token="invalid",
        collection_name="test_collection",
    )
    with pytest.raises(ValueError, match="Invalid Milvus token"):
        db.validate_config()


def test_validate_config_invalid_collection_name():
    db = MilvusVectorDB(
        url=config.milvus_url,
        token=config.milvus_token,
        collection_name="invalid",
    )
    with pytest.raises(ValueError, match="Invalid Milvus collection name"):
        db.validate_config()
