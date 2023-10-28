from .interface import EmbeddingModel
from huggingface_hub import InferenceClient
from pydantic import BaseModel
from typing import Literal


class HuggingFaceModel(EmbeddingModel, BaseModel):
    type: Literal["huggingface"] = "huggingface"
    token: str
    model: str
    batch_size: int = 128
    _client: InferenceClient

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._client = InferenceClient(token=self.token)

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = self._client.feature_extraction(text=texts, model=self.model)  # type: ignore
        return response.tolist()
