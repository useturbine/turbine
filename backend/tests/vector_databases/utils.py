import random
from turbine.vector_databases import Milvus, Pinecone
from ..config import config


def create_embedding():
    return [random.uniform(0, 1) for _ in range(1536)]


metadata = {
    "string": "value",
    "number": 123,
    "boolean": True,
    "list": ["a", "b", "c"],
}


def create_instance(type: str):
    if type == "pinecone":
        return Pinecone(
            api_key=config.pinecone_api_key,
            environment="gcp-starter",
            index_name="test-index",
        )
    elif type == "milvus":
        return Milvus(
            url=config.milvus_url,
            token=config.milvus_token,
            collection_name="test_collection",
        )
    else:
        raise ValueError("Invalid type")
