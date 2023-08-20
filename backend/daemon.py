from src.daemon.daemon import Daemon
from src.embedding_model.openai import OpenAIModel
from src.vectordb.milvus import MilvusVectorDB
from src.datasource.debezium import Debezium
from config import Config

openai_model = OpenAIModel(api_key=Config.openai_api_key)
vector_db = MilvusVectorDB(url=Config.milvus_url)
debezium = Debezium(debezium_url=Config.debezium_url, kafka_url=Config.kafka_url)

daemon = Daemon(debezium=debezium, embedding_model=openai_model, vector_db=vector_db)
daemon.run()
