from abc import abstractmethod


class EmbeddingModel:
    batch_size: int

    @abstractmethod
    def validate_config(self) -> None:
        ...

    @abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        ...
