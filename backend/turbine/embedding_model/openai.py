from .interface import EmbeddingModel
import openai
from typing import List
from pydantic import BaseModel
from typing import Literal


class OpenAIModel(EmbeddingModel, BaseModel):
    type: Literal["openai"]
    api_key: str
    model: str

    def __init__(self, **data) -> None:
        super().__init__(**data)
        openai.api_key = self.api_key

    def get_embedding(self, text: str) -> List[float]:
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]  # type: ignore
