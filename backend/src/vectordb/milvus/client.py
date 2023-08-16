from pymilvus import Collection, MilvusClient
from typing import Dict, Literal, List


class Client:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.client = MilvusClient(
            user=user,
            password=password,
            host=host,
            port=port,
        )

    def create_collection(
        self, name: str, id_type: Literal["int", "str"], dimension: int
    ):
        self.client.create_collection(
            collection_name=name, id_type=id_type, dimension=dimension
        )

    @staticmethod
    def create_index(collection_name: str, params: Dict):
        Collection(collection_name).create_index(
            field_name="vector", index_params=params
        )

    def insert(self, collection_name: str, data: List[Dict]):
        return self.client.insert(collection_name=collection_name, data=data)

    def search(self, collection_name: str, data, top_k, params):
        results = Collection(collection_name).search(
            data=data, anns_field=field, limit=top_k, param=params
        )
        return [h for h in results[0]]
