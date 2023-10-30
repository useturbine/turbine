from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from turbine.data_sources import S3
from turbine.vector_databases import Milvus, Pinecone
from turbine.embedding_models import HuggingFace, OpenAI


VectorDatabase = Milvus | Pinecone
EmbeddingModel = HuggingFace | OpenAI
DataSource = S3


class PipelineSchema(BaseModel):
    name: str
    description: Optional[str] = None
    vector_database: VectorDatabase
    embedding_model: EmbeddingModel
    data_source: DataSource

    def validate_config(self) -> None:
        self.data_source.validate_config()
        self.embedding_model.validate_config()
        self.vector_database.validate_config()
        if (
            self.embedding_model.embedding_dimension
            != self.vector_database.embedding_dimension
        ):
            raise ValueError(
                "Embedding model and vector database must have the same embedding dimension"
            )


class PipelineSchemaGet(PipelineSchema):
    id: UUID
