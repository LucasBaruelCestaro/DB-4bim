from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database as MongoDatabase
from typing import Optional
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()


class Database:
    _client: Optional[MongoClient] = None
    _db: Optional[MongoDatabase] = None

    @classmethod
    def connect(cls) -> None:
        if cls._client is None:
            uri = os.getenv("MONGO_URI")
            db_name = os.getenv("MONGO_DB")

            if not uri or not db_name:
                raise ValueError("Variáveis MONGO_URI e MONGO_DB não definidas no .env")

            cls._client = MongoClient(uri)
            cls._db = cls._client[db_name]

    @classmethod
    def get_collection(cls, name: str) -> Collection:
        if cls._db is None:
            cls.connect()
        return cls._db[name]

    @classmethod
    def close(cls) -> None:
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

