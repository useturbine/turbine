from .interface import EmbeddingModel
from huggingface_hub import InferenceClient
from typing import List
from pydantic import BaseModel
from typing import Literal


class HuggingFaceModel(EmbeddingModel, BaseModel):
    type: Literal["huggingface"]
    token: str
    model: str
    _client: InferenceClient

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._client = InferenceClient(token=self.token)

    def get_embedding(self, text: str) -> List[float]:
        response = self._client.feature_extraction(text=[text], model=self.model)  # type: ignore
        return response.tolist()
