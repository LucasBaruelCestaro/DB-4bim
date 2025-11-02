import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import Database
from models.grimorio import Grimorio

class GrimorioDAO:
    COLLECTION_NAME = "grimorios"

    def __init__(self):
        self.collection = Database.get_collection(self.COLLECTION_NAME)

    def create(self, grimorio: Grimorio) -> int:
        data = grimorio.to_dict_encrypted(global_secret=os.getenv("GLOBAL_KEY"))
        result = self.collection.insert_one(data)
        return result.inserted_id
    
    def read_all(self) -> list[Grimorio]:
        grimorios = []

        for data in self.collection.find():
            grimorio = Grimorio.from_dict_encrypted(data)
            grimorios.append(grimorio)

        return grimorios
    
    def read_by_name(self, title: str) -> Grimorio | None:
        data = self.collection.find_one({"title": title})
        if data:
            return Grimorio.from_dict_encrypted(data)
        return None


    def update(self, grimorio: Grimorio) -> bool:
        global_secret = os.getenv("GLOBAL_KEY")

        data = grimorio.to_dict_encrypted(global_secret)

        result = self.collection.update_one(
            {"title": grimorio.title},
            {"$set": data}
        )

        return result.modified_count > 0