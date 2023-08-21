from typing import List
from abc import abstractmethod
from src.datasource.interface import DataSourceUpdate
from kafka.consumer.fetcher import ConsumerRecord


class DebeziumConnector:
    @abstractmethod
    def validate_config(self, config: dict) -> bool:
        ...

    @abstractmethod
    def add_connector(self, id: int, config: dict) -> None:
        ...

    @abstractmethod
    def get_topics(self) -> List[str]:
        ...

    @abstractmethod
    def parse_message(self, message: ConsumerRecord) -> DataSourceUpdate:
        ...
