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
    _bucket: str
    _prefix: str

    def __init__(self, **data):
        super().__init__(**data)
        self._s3 = boto3.client(
            "s3",
            aws_access_key_id=Config.aws_access_key_id,
            aws_secret_access_key=Config.aws_secret_access_key,
        )
        parsed = urlparse(self.url)
        self._bucket = parsed.netloc
        self._prefix = parsed.path.lstrip("/")

    def get_keys(self) -> list[str]:
        keys = []
        continuation_token = None

        while True:
            if continuation_token is None:
                response = self._s3.list_objects_v2(
                    Bucket=self._bucket, Prefix=self._prefix
                )
            else:
                response = self._s3.list_objects_v2(
                    Bucket=self._bucket,
                    Prefix=self._prefix,
                    ContinuationToken=continuation_token,
                )

            if "Contents" in response:
                for obj in response["Contents"]:
                    keys.append(obj["Key"])

            if not response["IsTruncated"]:
                break
            continuation_token = response["NextContinuationToken"]

        return keys

    def get_documents(self, key: str) -> list[DataSourceDocument]:
        response = self._s3.get_object(Bucket=self._bucket, Key=key)
        text = response["Body"].read().decode("utf-8")
        return [
            DataSourceDocument(
                id=hashlib.sha256(document.text.encode("utf-8")).hexdigest(),
                text=document.text,
                metadata=document.metadata,
            )
            for document in self.splitter.split(text)
        ]
