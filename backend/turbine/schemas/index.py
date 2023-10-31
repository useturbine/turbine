from pydantic import BaseModel
from turbine.vector_databases import Milvus, Pinecone
from turbine.embedding_models import HuggingFace, OpenAI
from uuid import UUID


VectorDatabase = Milvus | Pinecone
EmbeddingModel = HuggingFace | OpenAI


class IndexSchema(BaseModel):
    name: str
    embedding_model: EmbeddingModel
    vector_database: VectorDatabase

    def validate_config(self) -> None:
        self.embedding_model.validate_config()
        self.vector_database.validate_config()
        if (
            self.embedding_model.embedding_dimension
            != self.vector_database.embedding_dimension
        ):
            raise ValueError(
                "Embedding model and vector database must have the same embedding dimension"
            )


class IndexSchemaGet(IndexSchema):
    id: UUID
