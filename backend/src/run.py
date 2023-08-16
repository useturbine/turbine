from vectordb.milvus.client import Client

client = Client(host="localhost", port=19530, user="root", password="Milvus")
collections = client.client.list_collections()
print(collections)
