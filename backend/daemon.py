from src.daemon.daemon import Daemon
from src.embedding_model.openai import OpenAIModel
from src.vectordb.milvus import MilvusVectorDB
from config import Config

openai_model = OpenAIModel(api_key=Config.openai_api_key)
vector_db = MilvusVectorDB(url=Config.milvus_url)

daemon = Daemon(
    kafka_url=Config.kafka_url, embedding_model=openai_model, vector_db=vector_db
)
daemon.run()
