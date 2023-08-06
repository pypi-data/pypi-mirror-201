from datetime import datetime

try:
    from pymongo import MongoClient
    from bson import Binary
except ImportError:
    pass

from stash.options import StashOptions
from stash.storages.storage import Storage


class MongoDbStorage(Storage):
    def __init__(self, options: StashOptions):
        super().__init__(options)
        self.client = MongoClient(
            self.options.mongo_dsn  # "mongodb://localhost:27017/"
        )
        self.db = self.client.cache_storage
        self.cache_items = self.db.cache_items
        self.cache_items.create_index(
            "timestamp", expireAfterSeconds=self.options.cache_max_age
        )

    def exists(self, key: str) -> bool:
        return self.cache_items.find_one({"_id": key}) is not None

    def purge(self, cutoff: int):
        pass

    def clear(self):
        self.cache_items.drop()

    def close(self):
        self.client.close()

    def write(self, key: str, content):
        item = {"data": Binary(content), "timestamp": datetime.utcnow()}
        self.cache_items.update_one({"_id": key}, {"$set": item}, upsert=True)

    def read(self, key: str):
        item = self.cache_items.find_one({"_id": key})
        if item:
            return item["data"]
        return None

    def rm(self, key: str):
        pass
