from turbine.vector_databases import VectorDatabase
from weaviate import Client, AuthApiKey


class Weaviate(VectorDatabase):
    url: str
    api_key: str

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.client = Client(
            url=self.url, auth_client_secret=AuthApiKey(api_key=self.api_key)
        )
