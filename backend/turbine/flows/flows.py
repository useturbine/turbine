from prefect import flow, task, unmapped
from turbine.data_source import DataSource, Document
from turbine.schema import PipelineSchema
from turbine.vector_database import VectorDatabase, VectorItem
from turbine.embedding_model import EmbeddingModel
from more_itertools import flatten, batched


@task
def get_keys(data_source: DataSource) -> list[str]:
    return data_source.get_keys()


@task
def get_documents(data_source: DataSource, key: str) -> list[Document]:
    return [document for document in data_source.get_documents(key)]


class DocumentWithEmbedding(Document):
    embedding: list[float]


@task
def create_embeddings(
    embedding_model: EmbeddingModel, documents: list[Document]
) -> list[DocumentWithEmbedding]:
    embeddings = embedding_model.get_embeddings(
        [document.text for document in documents]
    )
    return [
        DocumentWithEmbedding(
            **document.model_dump(),
            embedding=embedding,
        )
        for document, embedding in zip(documents, embeddings)
    ]


@task
def store_embeddings(
    vector_database: VectorDatabase,
    documents: list[DocumentWithEmbedding],
) -> None:
    vector_database.insert(
        [
            VectorItem(
                id=document.id,
                vector=document.embedding,
                metadata=document.metadata,
            )
            for document in documents
        ]
    )


@flow(name="run-pipeline", log_prints=True)
def run_pipeline(pipeline: PipelineSchema):
    keys = get_keys(pipeline.data_source)

    documents_futures = get_documents.map(unmapped(pipeline.data_source), keys)  # type: ignore
    documents = flatten([item.result() for item in documents_futures])

    embeddings_futures = create_embeddings.map(
        unmapped(pipeline.embedding_model),  # type: ignore
        batched(documents, pipeline.embedding_model.batch_size),  # type: ignore
    )
    embeddings = flatten([item.result() for item in embeddings_futures])

    store_embeddings.map(
        unmapped(pipeline.vector_database),  # type: ignore
        batched(embeddings, pipeline.vector_database.batch_size),  # type: ignore
    )
