from turbine.embedding_models import OpenAIModel
from ..config import config


def test_init():
    model = OpenAIModel(
        api_key=config.openai_api_key,
        model="text-embedding-ada-002",
    )
    assert model is not None


def test_get_embeddings():
    model = OpenAIModel(
        api_key=config.openai_api_key,
        model="text-embedding-ada-002",
    )
    embeddings = model.get_embeddings(["Hello world"])
    assert embeddings is not None
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 1536
