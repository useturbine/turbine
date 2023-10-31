from turbine.vector_databases import VectorDatabase, VectorDocument
from turbine.embedding_models import EmbeddingModel
from prefect import task
from turbine.types import Document


@task
def create_embeddings(
    embedding_model: EmbeddingModel, documents: list[Document]
) -> list[VectorDocument]:
    embeddings = embedding_model.get_embeddings(
        [document.content for document in documents]
    )
    return [
        VectorDocument(
            **document.model_dump(),
            embedding=embedding,
        )
        for document, embedding in zip(documents, embeddings)
    ]


@task
def store_embeddings(
    vector_database: VectorDatabase,
    documents: list[VectorDocument],
) -> None:
    vector_database.insert(documents)
