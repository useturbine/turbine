from turbine.schemas import IndexSchemaGet
from prefect import flow, unmapped
from .common import create_embeddings, store_embeddings
from more_itertools import flatten, batched
from turbine.types import Document
from turbine.file_parsers import parse_file
from minio import Minio
from io import BytesIO


minio = Minio(
    "minio:9000",
    access_key="admin",
    secret_key="secretpassword",
    secure=False,
)


@flow(name="process-files", log_prints=True)
def process_files(index: IndexSchemaGet, files: list[str]):
    documents: list[Document] = []
    for file in files:
        response = minio.get_object(str(index.id), file)
        documents.extend(
            [
                Document(
                    id=document.id,
                    content=document.content,
                    metadata=dict(**document.metadata, filename=file),
                )
                for document in parse_file(file=BytesIO(response.read()), filename=file)
            ]
        )

    embeddings_futures = create_embeddings.map(
        unmapped(index.embedding_model),  # type: ignore
        batched(documents, index.embedding_model._batch_size),  # type: ignore
    )
    embeddings = flatten([item.result() for item in embeddings_futures])

    store_embeddings.map(
        unmapped(index.vector_database),  # type: ignore
        batched(embeddings, index.vector_database._batch_size),  # type: ignore
    )
