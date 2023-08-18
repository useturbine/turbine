from src.datasource.interface import DataSource

from pymongo import MongoClient
from typing import Iterator, Tuple, Optional
from datetime import datetime


def flatten_dict(
    nested_dict: dict, parent_key: Optional[str] = None, separator: str = "."
) -> dict:
    """
    Flatten a nested dictionary into a single level.
    """
    items = []
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


class MongoDataSource(DataSource):
    def __init__(
        self,
        uri: str,
        database: str,
        collection: str,
        updated_at_field: Optional[str] = None,
    ) -> None:
        self.client = MongoClient(uri)
        self.collection = self.client[database][collection]
        self.updated_at_field = updated_at_field

    @staticmethod
    def format_document(doc) -> Tuple[str, str]:
        flattened_doc = flatten_dict(doc)
        return (
            str(doc["_id"]),
            "\n".join(f"{k}: {v}" for k, v in flattened_doc.items()),
        )

    def get_documents(
        self, updated_since: Optional[datetime] = None
    ) -> Iterator[Tuple[str, str]]:
        if updated_since:
            if not self.updated_at_field:
                raise Exception(
                    "updated_at_field must be provided if using updated_since"
                )
            results = self.collection.find(
                {self.updated_at_field: {"$gt": updated_since}}
            )
        else:
            results = self.collection.find()

        for doc in results:
            yield self.format_document(doc)

    def listen_for_updates(self) -> Iterator[Tuple[str, Optional[str]]]:
        change_stream = self.collection.watch(full_document="updateLookup")

        for change in change_stream:
            if change["operationType"] == "delete":
                yield (str(change["documentKey"]["_id"]), None)
            else:
                yield self.format_document(change["fullDocument"])
