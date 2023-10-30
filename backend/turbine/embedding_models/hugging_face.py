from .interface import EmbeddingModel
from huggingface_hub import InferenceClient
from huggingface_hub.utils import BadRequestError, HfHubHTTPError
from typing import Literal


class HuggingFaceModel(EmbeddingModel):
    type: Literal["huggingface"] = "huggingface"
    token: str
    model: str
    batch_size: int = 128
    _client: InferenceClient

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._client = InferenceClient(token=self.token)

    def validate_config(self) -> None:
        try:
            self._client.get_model_status(self.model)
        except HfHubHTTPError:
            raise ValueError("Invalid HuggingFace model")
        try:
            self.get_sample_embedding()
        except BadRequestError:
            raise ValueError("Invalid HuggingFace token")

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = self._client.feature_extraction(text=texts, model=self.model)  # type: ignore
        return response.tolist()
