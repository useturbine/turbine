import magic
from typing import IO
from turbine.types import Document
from .interface import FileParser
from langchain.document_loaders.unstructured import UnstructuredAPIFileIOLoader
from turbine.types import Document
import hashlib
from unstructured.file_utils.filetype import FileType, detect_filetype


custom_parsers: list[FileParser] = []
custom_parser_mimes: list[str] = [parser.mime for parser in custom_parsers]


def get_mime(file: IO) -> str:
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    return mime


def validate_file(file: IO, filename: str) -> bool:
    mime = get_mime(file)
    if mime in custom_parser_mimes:
        return True
    filetype = detect_filetype(file=file, file_filename=filename)
    if filetype == FileType.UNK or filetype == FileType.EMPTY:
        return False
    return True


def parse_file(file: IO, filename: str) -> list[Document]:
    mime = get_mime(file)

    if mime in custom_parser_mimes:
        parser = custom_parsers[custom_parser_mimes.index(mime)]
        return [
            Document(
                id=document.id,
                content=document.content,
                metadata=dict(**document.metadata, filename=filename),
            )
            for document in parser.get_documents(file)
        ]

    unstructured_loader = UnstructuredAPIFileIOLoader(
        url="http://unstructured:8000/general/v0/general",
        file=file,
        file_filename=filename,
    )
    documents = [
        Document(
            id=hashlib.sha256(document.page_content.encode("utf-8")).hexdigest(),
            content=document.page_content,
            metadata=document.metadata,
        )
        for document in unstructured_loader.load_and_split()
    ]
    return documents
