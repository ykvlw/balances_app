import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["token_balance_db"]


def get_db() -> Database:
    return db


def get_db_collection() -> Collection:
    return db["balances"]
