from turbine.vector_db.milvus import MilvusVectorDB
from turbine.vector_db.pinecone import PineconeVectorDB
from config import Config
from turbine.vector_db.interface import VectorDB
from turbine.schema import VectorDBSchema
import uuid
import shortuuid


def get_vector_db(vector_db: VectorDBSchema) -> VectorDB:
    if vector_db.type == "milvus":
        return MilvusVectorDB(url=vector_db.config.url, token=vector_db.config.token)
    elif vector_db.type == "pinecone":
        return PineconeVectorDB(
            api_key=vector_db.config.api_key,
            environment=vector_db.config.environment,
        )
    else:
        raise ValueError("Invalid vector DB")
