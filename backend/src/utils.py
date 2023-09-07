from src.vector_db.milvus import MilvusVectorDB
from src.vector_db.pinecone import PineconeVectorDB
from config import Config
from src.vector_db.interface import VectorDB


def get_vector_db(vector_db: str) -> VectorDB:
    if vector_db == "milvus":
        return MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)
    elif vector_db == "pinecone":
        return PineconeVectorDB(
            api_key=Config.pinecone_token, environment=Config.pinecone_environment
        )
    else:
        raise ValueError("Invalid vector DB")
