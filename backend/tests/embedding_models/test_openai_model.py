from turbine.embedding_models import OpenAIModel
from ..config import config
from .common import texts


def create_instance():
    return OpenAIModel(
        api_key=config.openai_api_key,
        model="text-embedding-ada-002",
    )


def test_init():
    model = create_instance()
    assert model is not None


def test_get_embeddings():
    model = create_instance()
    embeddings = model.get_embeddings(texts)
    assert embeddings is not None
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1536 and len(embeddings[1]) == 1536
    assert embeddings[0] != embeddings[1]
