import boto3
from src.datasource.interface import DataSource
from typing import Iterator, Tuple, Optional


class S3DataSource(DataSource):
    def __init__(self, bucket_name: str, prefix: Optional[str] = None) -> None:
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.prefix = prefix

    @staticmethod
    def format_object(key: str, content: bytes) -> Tuple[str, str]:
        return key, content.decode('utf-8')

    def get_documents(self) -> Iterator[Tuple[str, str]]:
        paginator = self.s3.get_paginator('list_objects_v2')
        operation_parameters = {'Bucket': self.bucket_name}

        if self.prefix:
            operation_parameters['Prefix'] = self.prefix

        page_iterator = paginator.paginate(**operation_parameters)

        for page in page_iterator:
            for item in page.get('Contents', []):
                key = item['Key']
                response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
                content = response['Body'].read()
                yield self.format_object(key, content)

    def listen_for_updates(self) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError("no easy way.")
