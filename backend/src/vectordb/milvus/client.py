from pymilvus import Collection
from pymilvus import MilvusClient
# from MilvusException import CollectionNotExistException

class Client():
    def __init__(self, **kwargs):
        self.client = MilvusClient(
            uri=kwargs.get('uri'),
            user=kwargs.get('user'),
            password=kwargs.get('password'))

    def create_collection(self, name, params):
        return self.client.create_collection(name, params)

    @staticmethod
    def create_index(collection, field, params, index_name):
        Collection(collection).create_index(field, params, index_name)

    def insert(self, collection, params):
        self.client.insert(collection, params)

    def search(self, collection, field, data, top_k, params):
        results = Collection(collection).search(data=data, anns_field=field, limit=top_k, param=params)
        return [h for h in results[0]]