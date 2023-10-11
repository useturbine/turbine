from .interface import EmbeddingModel
import openai
from typing import List


class OpenAIModel(EmbeddingModel):
    def __init__(self, api_key: str, model: str) -> None:
        openai.api_key = api_key
        self.model = model

    def get_embedding(self, text: str) -> List[float]:
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]  # type: ignore
