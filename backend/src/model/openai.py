from model.interface import Model
import tiktoken
import openai
from typing import List


class OpenAIModel(Model):
    name = "openai"
    embedding_dimension = 1536

    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

    def get_embedding(self, text: str) -> List[float]:
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]  # type: ignore

    @staticmethod
    def get_num_tokens(text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
