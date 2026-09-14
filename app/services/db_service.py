import os
from pymongo import MongoClient

# Fetch MongoDB URI from environment variables
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/astrology_app")

# Initialize MongoDB Client
try:
    client = MongoClient(MONGODB_URI)
    db = client.get_database() # Gets the default database from URI
    
    # Collections
    cache_collection = db["daily_cache"]
    token_collection = db["token_usage"]
    
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    client = None
    db = None
    cache_collection = None
    token_collection = None

class DBService:
    @staticmethod
    def get_cache(key: str) -> dict:
        if cache_collection is not None:
            return cache_collection.find_one({"_id": key})
        return None

    @staticmethod
    def set_cache(key: str, data: dict):
        if cache_collection is not None:
            # We store the data under a document with _id = key
            doc = {"_id": key, "data": data}
            cache_collection.update_one({"_id": key}, {"$set": doc}, upsert=True)

    @staticmethod
    def increment_tokens(tokens_used: int) -> int:
        if token_collection is not None:
            # We keep a single document for total token usage
            doc = token_collection.find_one_and_update(
                {"_id": "total_usage"},
                {"$inc": {"count": tokens_used}},
                upsert=True,
                return_document=True
            )
            return doc.get("count", 0)
        return 0

    @staticmethod
    def get_total_tokens() -> int:
        if token_collection is not None:
            doc = token_collection.find_one({"_id": "total_usage"})
            if doc:
                return doc.get("count", 0)
        return 0
