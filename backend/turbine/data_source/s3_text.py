from .interface import DataSource, DataSourceDocument
from .splitter import RecursiveSplitter
from pydantic import BaseModel
from typing import Literal, Any
import boto3
from urllib.parse import urlparse
from config import Config
import hashlib


class S3TextDataSource(DataSource, BaseModel):
    type: Literal["s3_text"]
    url: str
    splitter: RecursiveSplitter
    _s3: Any

    def __init__(self, **data):
        super().__init__(**data)
        self._s3 = boto3.resource(
            "s3",
            aws_access_key_id=Config.aws_access_key_id,
            aws_secret_access_key=Config.aws_secret_access_key,
        )

    def get_documents(self) -> list[DataSourceDocument]:
        parsed = urlparse(self.url)
        bucket = parsed.netloc
        key = parsed.path.lstrip("/")

        obj = self._s3.Object(bucket, key)
        text = obj.get()["Body"].read().decode("utf-8")
        return [
            DataSourceDocument(
                id=hashlib.sha256(document.text.encode("utf-8")).hexdigest(),
                text=document.text,
                metadata=document.metadata,
            )
            for document in self.splitter.split(text)
        ]
