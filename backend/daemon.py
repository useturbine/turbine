from src.daemon.daemon import Daemon
from src.embedding_model.openai import OpenAIModel
from src.vectordb.milvus import MilvusVectorDB
from src.datasource.debezium.debezium import DebeziumDataSource
from config import Config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
)

openai_model = OpenAIModel(api_key=Config.openai_api_key)
vector_db = MilvusVectorDB(url=Config.milvus_url, token=Config.milvus_token)
debezium = DebeziumDataSource(
    debezium_url=Config.debezium_url, kafka_url=Config.kafka_url
)

daemon = Daemon(data_source=debezium, embedding_model=openai_model, vector_db=vector_db)
daemon.run()
