from turbine.vector_databases import VectorDatabase, VectorItem
from turbine.embedding_models import EmbeddingModel
from prefect import task
from turbine.types import Document


@task
def create_embeddings(
    embedding_model: EmbeddingModel, documents: list[Document]
) -> list[VectorItem]:
    embeddings = embedding_model.get_embeddings(
        [document.content for document in documents]
    )
    return [
        VectorItem(
            **document.model_dump(),
            embedding=embedding,
        )
        for document, embedding in zip(documents, embeddings)
    ]


@task
def store_embeddings(
    vector_database: VectorDatabase,
    documents: list[VectorItem],
) -> None:
    vector_database.insert(
        [
            VectorItem(
                id=document.id,
                embedding=document.embedding,
                metadata=document.metadata,
            )
            for document in documents
        ]
    )
