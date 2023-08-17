from pymongo import MongoClient
from datasource.interface import DataSource
from typing import Iterator, Tuple


class MongoDataSource(DataSource):
    def __init__(self, uri: str, database: str, collection: str) -> None:
        self.client = MongoClient(uri)
        self.collection = self.client[database][collection]
        self.last_fetched_time = None

    @staticmethod
    def format_document(doc) -> str:
        """Format a Mongo doc to a string where each key-value pair is on a new line."""
        return "\n".join(f"{k}: {v}" for k, v in doc.items())

    def get_all_documents(self) -> Iterator[Tuple[str, str]]:
        for doc in self.collection.find():
            yield (str(doc["_id"]), self.format_document(doc))

    def get_new_documents(self, db_name, collection):
        """Retrieve documents that were added/updated after the last fetched time."""
        db = self.client[db_name]
        collection = db[collection]

        query = {}
        if self.last_fetched_time:
            # assumption: documents have a 'timestamp' field to track when they were added/updated.
            query["timestamp"] = {"$gt": self.last_fetched_time}

        new_documents = list(collection.find(query))
        if new_documents:
            self.last_fetched_time = max(doc["timestamp"] for doc in new_documents)

        return new_documents
