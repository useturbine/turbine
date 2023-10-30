import pytest
from tests.config import config
from turbine.vector_databases import PineconeVectorDB


def test_validate_config_invalid_api_key():
    db = PineconeVectorDB(
        api_key="invalid",
        environment="gcp-starter",
        index_name="test-index",
    )
    with pytest.raises(ValueError, match="Invalid Pinecone API key"):
        db.validate_config()


def test_validate_config_invalid_environment():
    db = PineconeVectorDB(
        api_key=config.pinecone_api_key,
        environment="invalid",
        index_name="test-index",
    )
    with pytest.raises(ValueError, match="Invalid Pinecone environment"):
        db.validate_config()


def test_validate_config_invalid_index_name():
    db = PineconeVectorDB(
        api_key=config.pinecone_api_key,
        environment="gcp-starter",
        index_name="invalid",
    )
    with pytest.raises(ValueError, match="Invalid Pinecone index name"):
        db.validate_config()
