from prefect import flow, task, unmapped
from turbine.data_sources import DataSource
from turbine.types import Document
from turbine.schemas import DataSourceSchema, IndexSchema
from more_itertools import flatten, batched
from .common import create_embeddings, store_embeddings


@task
def get_keys(data_source: DataSource) -> list[str]:
    return data_source.get_keys()


@task
def get_documents(data_source: DataSource, key: str) -> list[Document]:
    return [document for document in data_source.get_documents(key)]


@flow(name="sync-data-source", log_prints=True)
def sync_data_source(index: IndexSchema, data_source: DataSourceSchema):
    keys = get_keys(data_source.data_source)

    documents_futures = get_documents.map(unmapped(data_source.data_source), keys)  # type: ignore
    documents = flatten([item.result() for item in documents_futures])

    embeddings_futures = create_embeddings.map(
        unmapped(index.embedding_model),  # type: ignore
        batched(documents, index.embedding_model._batch_size),  # type: ignore
    )
    embeddings = flatten([item.result() for item in embeddings_futures])

    store_embeddings.map(
        unmapped(index.vector_database),  # type: ignore
        batched(embeddings, index.vector_database._batch_size),  # type: ignore
    )
