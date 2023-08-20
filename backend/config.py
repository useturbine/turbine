from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    kafka_url = os.getenv("KAFKA_URL", "localhost:9092")
    debezium_url = os.getenv("DEBEZIUM_URL", "http://localhost:8083")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    milvus_url = os.getenv("MILVUS_URL", "tcp://localhost:19530")
