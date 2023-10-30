from turbine.embedding_models import HuggingFace, OpenAI
from ..config import config


texts = ["Hello world", "Some other text"]


def create_instance(type: str):
    if type == "huggingface":
        return HuggingFace(
            token=config.huggingface_token,
            model="BAAI/bge-large-en-v1.5",
        )
    elif type == "openai":
        return OpenAI(
            api_key=config.openai_api_key,
            model="text-embedding-ada-002",
        )
    else:
        raise ValueError("Invalid type")
