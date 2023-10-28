from turbine.embedding_models import HuggingFaceModel, OpenAIModel
from ..config import config


texts = ["Hello world", "Some other text"]


def create_instance(type: str):
    if type == "huggingface":
        return HuggingFaceModel(
            token=config.huggingface_token,
            model="BAAI/bge-large-en-v1.5",
        )
    elif type == "openai":
        return OpenAIModel(
            api_key=config.openai_api_key,
            model="text-embedding-ada-002",
        )
    else:
        raise ValueError("Invalid type")
