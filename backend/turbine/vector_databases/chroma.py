from turbine.vector_databases import VectorDatabase
from chromadb import HttpClient
from chromadb.config import Settings


class Chroma(VectorDatabase):
    host: str
    port: int
    token: str

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.client = HttpClient(
            host=self.host,
            port=str(self.port),
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                chroma_client_auth_credentials=self.token,
            ),
        )
