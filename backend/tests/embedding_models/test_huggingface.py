import pytest
from tests.config import config
from turbine.embedding_models import HuggingFaceModel


def test_validate_config_invalid_token():
    model = HuggingFaceModel(
        token="invalid",
        model="BAAI/bge-large-en-v1.5",
    )
    with pytest.raises(ValueError, match="Invalid HuggingFace token"):
        model.validate_config()


def test_validate_config_invalid_model():
    model = HuggingFaceModel(
        token=config.huggingface_token,
        model="invalid",
    )
    with pytest.raises(ValueError, match="Invalid HuggingFace model"):
        model.validate_config()
