from abc import abstractmethod
from typing import Iterator, Tuple


class DataSource:
    @abstractmethod
    def get_all_documents(self) -> Iterator[Tuple[str, str]]:
        pass

    @abstractmethod
    def get_new_documents(self) -> Iterator[Tuple[str, str]]:
        pass
