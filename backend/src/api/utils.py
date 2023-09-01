from src.vector_db.milvus import MilvusVectorDB
from src.vector_db.pinecone import PineconeVectorDB
from src.embedding_model.openai import OpenAIModel
from config import Config
from src.vector_db.interface import VectorDB


def get_vector_db(vector_db: str) -> VectorDB:
    if vector_db == "milvus":
        return MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)
    elif vector_db == "pinecone":
        return PineconeVectorDB(
            api_key=Config.pinecone_api_key, environment=Config.pinecone_environment
        )
    else:
        raise ValueError("Invalid vector DB")


def get_embedding_model(embedding_model: str):
    if embedding_model == "openai":
        return OpenAIModel(api_key=Config.openai_api_key)
    else:
        raise ValueError("Invalid embedding model")
