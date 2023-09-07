from .interface import EmbeddingModel
from huggingface_hub import InferenceClient
from typing import List


class HuggingFaceModel(EmbeddingModel):
    def __init__(self, token: str, model: str) -> None:
        self.model = model
        self.client = InferenceClient(token=token)

    def get_embedding(self, text: str) -> List[float]:
        response = self.client.feature_extraction(text=[text], model=self.model)  # type: ignore
        return response.tolist()
