import pytest
from tests.config import config
from turbine.embedding_models import OpenAI


def test_validate_config_invalid_api_key():
    model = OpenAI(
        api_key="invalid",
        model="text-embedding-ada-002",
    )
    with pytest.raises(ValueError, match="Invalid OpenAI API key"):
        model.validate_config()


def test_validate_config_invalid_model():
    model = OpenAI(
        api_key=config.openai_api_key,
        model="invalid",
    )
    with pytest.raises(ValueError, match="Invalid OpenAI model"):
        model.validate_config()
