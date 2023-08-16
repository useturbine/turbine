from pymilvus import Collection
from pymilvus import MilvusClient
# from MilvusException import CollectionNotExistException

class Client():
    def __init__(self):
        self.client = MilvusClient(
            uri='http://localhost:19530',
            user='root',
            password='Milvus')

        self.collections = {}

    def create_collection(self, name, params):
        # collection_param = {
        #     "fields": [
        #         {"name": "vector", "type": DataType.FLOAT_VECTOR, "params": {"dim": dimension},
        #          "indexes": [{"metric_type": "L2"}]}
        #     ],
        #     "segment_row_count": 4096,
        #     "auto_id": True
        # }

        if name in self.collections:
            return self.collections[name]

        c = self.create_collection(name, params)
        self.collections[name] = c
        return c

    def create_index(self, name, field_name, params):
        """
        index_param = {
        "index_type": "IVF_SQ8",
        "metric_type": "L2",
        "params": {"nlist": 2048}
        }"""

        self.client.create_index(collection_name, "vector", index_param)

    def insert(self):
        # insert_param = {
        #     "fields": [
        #         {"name": "vector", "type": DataType.FLOAT_VECTOR, "values": vectors}
        #     ]
        # }

        self.client.insert(collection_name, insert_param)

    def search(self):
        # search_params = {
        #     "metric_type": "L2",
        #     "params": {"nprobe": 10}
        # }

        results = self.client.search(
            collection_name,
            {"vector": {"topk": top_k, "query": query_embedding, "params": search_params}})
        return [h for h in results[0]]