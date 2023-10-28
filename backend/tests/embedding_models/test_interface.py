from .utils import texts, create_instance
import pytest


@pytest.mark.parametrize(
    "type",
    [
        "openai",
        "huggingface",
    ],
)
class TestEmbeddingModel:
    def test_init(self, type: str):
        model = create_instance(type)
        assert model is not None

    def test_validate_config(self, type: str):
        model = create_instance(type)
        model.validate_config()

    def test_embedding_dimension(self, type: str):
        model = create_instance(type)
        assert model.embedding_dimension is not None
        assert isinstance(model.embedding_dimension, int)
        assert model.embedding_dimension > 0

    def test_get_embeddings(self, type: str):
        model = create_instance(type)
        embeddings = model.get_embeddings(texts)
        assert embeddings is not None
        assert len(embeddings) == 2
        assert (
            len(embeddings[0]) == model.embedding_dimension
            and len(embeddings[1]) == model.embedding_dimension
        )
        assert embeddings[0] != embeddings[1]
