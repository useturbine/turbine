from src.vectordb.milvus import MilvusVectorDB
from src.vectordb.pinecone import PineconeVectorDB
from config import Config

# vector_db = MilvusVectorDB(url=Config.milvus_url)
vector_db = PineconeVectorDB(
    api_key=Config.pinecone_api_key, environment=Config.pinecone_environment
)

try:
    vector_db.drop_collection("testcollection")
except Exception as e:
    print(e)


vector_db.create_collection("testcollection", 3)
vector_db.insert("testcollection", [{"id": "1", "vector": [0.1, 0.2, 0.3]}])

response = vector_db.search("testcollection", [0.1, 0.2, 0.3], limit=10)
print(response)
