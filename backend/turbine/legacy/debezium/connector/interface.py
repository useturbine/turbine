from typing import List
from abc import abstractmethod
from turbine.data_sources.interface import Document
from kafka.consumer.fetcher import ConsumerRecord


class DebeziumConnector:
    @abstractmethod
    def validate_config(self, config) -> bool:
        ...

    @abstractmethod
    def add_connector(self, id: int, config) -> None:
        ...

    @abstractmethod
    def get_topics(self) -> List[str]:
        ...

    @abstractmethod
    def parse_message(self, message: ConsumerRecord) -> Document:
        ...
