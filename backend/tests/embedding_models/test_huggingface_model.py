from ..config import config
from turbine.embedding_models import HuggingFaceModel
from .common import texts


def create_instance():
    return HuggingFaceModel(
        token=config.huggingface_token,
        model="BAAI/bge-large-en-v1.5",
    )


def test_init():
    model = create_instance()
    assert model is not None


def test_get_embeddings():
    model = create_instance()
    embeddings = model.get_embeddings(texts)
    assert embeddings is not None
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1024 and len(embeddings[1]) == 1024
    assert embeddings[0] != embeddings[1]
