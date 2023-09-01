from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    postgres_url = os.getenv(
        "POSTGRES_URL", "postgres://admin:passwd@turbine-postgres:5432/turbine"
    )
    kafka_url = os.getenv("KAFKA_URL", "localhost:19092")
    debezium_url = os.getenv("DEBEZIUM_URL", "http://localhost:8083")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    milvus_url = os.getenv("MILVUS_URL", "tcp://localhost:19530")
    milvus_token = os.getenv("MILVUS_TOKEN", "")
    pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "dev")
