import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bson import ObjectId
from db.database import Database
from models.feiticeiro import Feiticeiro

class FeiticeiroDAO:
    COLLECTION_NAME = "feiticeiros"

    def __init__(self):
        self.collection = Database.get_collection(self.COLLECTION_NAME)

    def create(self, feiticeiro: Feiticeiro) -> Feiticeiro:
        data = feiticeiro.to_dict()
        result = self.collection.insert_one(data)
        feiticeiro.id = str(result.inserted_id)
        return feiticeiro

    def read_all(self) -> list[Feiticeiro]:
        feiticeiros_data = list(self.collection.find())
        feiticeiros = []
        for data in feiticeiros_data:
            data["id"] = str(data["_id"])
            data.pop("_id", None)
            feiticeiros.append(Feiticeiro.from_dict(data))
        return feiticeiros

    def read_by_id(self, feiticeiro_id: str) -> Feiticeiro | None:
        try:
            object_id = ObjectId(feiticeiro_id)
        except Exception:
            return None

        data = self.collection.find_one({"_id": object_id})
        if not data:
            return None

        data["id"] = str(data["_id"])
        data.pop("_id", None)
        return Feiticeiro.from_dict(data)

    def update(self, feiticeiro_id: str, feiticeiro: Feiticeiro) -> bool:
        try:
            object_id = ObjectId(feiticeiro_id)
        except Exception:
            return False

        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": feiticeiro.to_dict()}
        )
        return result.modified_count > 0

    def delete(self, feiticeiro_id: str) -> bool:
        try:
            object_id = ObjectId(feiticeiro_id)
        except Exception:
            return False

        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count > 0