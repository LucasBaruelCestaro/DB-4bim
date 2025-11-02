import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import Database
from models.feiticeiro import Feiticeiro


class FeiticeiroDAO:
    COLLECTION_NAME = "feiticeiros"

    def __init__(self):
        self.collection = Database.get_collection(self.COLLECTION_NAME)

    def create(self, feiticeiro: Feiticeiro) -> int:
        if feiticeiro.intID is not None:
            pass
        else:
            feiticeiro.intID = self._get_next_id()

        data = feiticeiro.to_dict()
        result = self.collection.insert_one(data)

        return result.inserted_id
    
    def read_all(self) -> list[Feiticeiro]:
        feiticeiros = []

        for data in self.collection.find():
            feiticeiro = Feiticeiro.from_dict(data)
            feiticeiros.append(feiticeiro)

        return feiticeiros
    
    def read_by_id(self, intID: int) -> Feiticeiro | None:
        data = self.collection.find_one({"intID": intID})
        if data:
            return Feiticeiro.from_dict(data)
        return None
    
    def update(self, feiticeiro: Feiticeiro) -> bool:
        if feiticeiro.intID is None:
            raise ValueError("O ID do feiticeiro não pode ser None para atualização.")

        data = feiticeiro.to_dict()
        result = self.collection.update_one(
            {"intID": feiticeiro.intID},
            {"$set": data}
        )

        return result.modified_count > 0
    
    def delete(self, intID: int) -> bool:
        result = self.collection.delete_one({"intID": intID})
        return result.deleted_count > 0

    def _get_next_id(self) -> int:
        last_feiticeiro = self.collection.find_one(
            sort=[("intID", -1)]
        )
        if last_feiticeiro and "intID" in last_feiticeiro:
            return last_feiticeiro["intID"] + 1
        else:
            return 1
