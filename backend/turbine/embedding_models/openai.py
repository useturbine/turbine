from .interface import EmbeddingModel
import openai
from openai.error import OpenAIError
from pydantic import BaseModel
from typing import Literal


class OpenAIModel(EmbeddingModel, BaseModel):
    type: Literal["openai"]
    api_key: str
    model: str
    batch_size: int = 128

    def __init__(self, **data) -> None:
        super().__init__(**data)
        openai.api_key = self.api_key

    def validate_config(self) -> None:
        try:
            openai.Model.list()
        except OpenAIError:
            raise ValueError("Invalid OpenAI API key")
        try:
            self.get_embeddings(["test"])
        except OpenAIError:
            raise ValueError("Invalid OpenAI model")

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = openai.Embedding.create(input=texts, model=self.model)
        return [item["embedding"] for item in response["data"]]  # type: ignore
