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

    def _get_next_id(self) -> int:
        last_feiticeiro = self.collection.find_one(
            sort=[("intID", -1)]
        )
        if last_feiticeiro and "intID" in last_feiticeiro:
            return last_feiticeiro["intID"] + 1
        else:
            return 1
        
if __name__ == "__main__":
    pass