from pymongo import MongoClient
from datetime import datetime
from src.datasource.interface import DataSource


class MongoDataSource(DataSource):
    def __init__(self, url):
        self.client = MongoClient(url)
        self.last_fetched_time = None

    def get_all_documents(self, db_name, collection):
        """Retrieve all documents from a given collection."""
        db = self.client[db_name]
        collection = db[collection]
        return list(collection.find())

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


mongo_client = MongoDataSource("mongodb://localhost:27017/")
all_docs = mongo_client.get_all_documents("", "")
print(all_docs)

new_docs = mongo_client.get_new_documents("", "")
print(new_docs)
