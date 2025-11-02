import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Optional, List
from models.feitico import Feitico
import bcrypt

class Grimorio:
    def __init__(self):
        self._title: Optional[str] = None
        self._author: Optional[str] = None
        self._description: Optional[str] = None
        self._feiticos: List[Feitico] = []
        self._hash_password: Optional[bytes] = None
        self._open: bool = False

    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        parsed = value.strip()

        if not parsed or len(parsed) < 3 or len(parsed) > 100:
            raise ValueError("Título inválido.")
        
        self._title = parsed

    @property
    def author(self) -> Optional[str]:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        parsed = value.strip()

        if not parsed or len(parsed) < 3 or len(parsed) > 50:
            raise ValueError("Autor inválido.")
        
        self._author = parsed

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        parsed = " ".join(value.strip().split())

        if not parsed or len(parsed) < 10 or len(parsed) > 500:
            raise ValueError("Descrição inválida.")
        
        self._description = parsed

    @property
    def feiticos(self) -> List[Feitico]:
        return self._feiticos

    @feiticos.setter
    def feiticos(self, value: List[Feitico]) -> None:
        if not isinstance(value, list):
            raise TypeError("Feitiços devem ser uma lista.")
        
        for item in value:
            if not isinstance(item, Feitico):
                raise TypeError("Todos os itens devem ser Feitico.")
            
        nomes = [f.name.lower() for f in value if f.name]

        if len(nomes) != len(set(nomes)):
            raise ValueError("Feitiços com nomes duplicados.")
        
        self._feiticos = value

    def set_password(self, password: str) -> None:
        if self._hash_password:
            raise PermissionError("Senha já definida.")
        
        self._hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        if not self._hash_password:
            raise ValueError("Nenhuma senha definida.")
        
        if bcrypt.checkpw(password.encode(), self._hash_password):
            self._open = True
            return True
        
        return False

    def close(self) -> None:
        self._open = False

    def adicionar_feitico(self, feitico: Feitico) -> None:
        if not self._open:
            raise PermissionError("Grimório selado.")
        
        if any(f.name.lower() == feitico.name.lower() for f in self._feiticos):
            raise ValueError(f"Feitiço '{feitico.name}' já existe.")
        
        self._feiticos.append(feitico)

    def listar_feiticos_visiveis(self, mage_level: int, global_secret: str) -> List[Feitico]:
        if not self._open:
            raise PermissionError("Grimório selado.")
        
        visiveis = []

        for f_enc in self._feiticos:
            try:
                f_obj = Feitico.from_encrypted_dict_by_mage_level(f_enc, mage_level, global_secret)
                visiveis.append(f_obj)
            except PermissionError:
                continue

        return visiveis

    def to_dict_encrypted(self, global_secret: str) -> dict:
        feiticos_serializados = []
        for f in self._feiticos:
            if isinstance(f, dict):
                feiticos_serializados.append(f)
            else:
                feiticos_serializados.append(f.to_encrypted_dict_by_level(global_secret))

        return {k: v for k, v in {
            "title": self._title,
            "author": self._author,
            "description": self._description,
            "hash_password": self._hash_password.decode("utf-8") if self._hash_password else None,
            "feiticos": feiticos_serializados
        }.items() if v is not None}

    @classmethod
    def from_dict_encrypted(cls, data: dict):
        obj = cls()
        obj._title = data.get("title")
        obj._author = data.get("author")
        obj._description = data.get("description")
        hash_str = data.get("hash_password")
        obj._hash_password = hash_str.encode("utf-8") if hash_str else None
        obj._feiticos = data.get("feiticos", [])

        return obj
    
if __name__ == "__main__":
    grimorio = Grimorio()
    grimorio.title = "Grimório dos Magos"
    grimorio.author = "Merlin"
    grimorio.description = "Um grimório antigo cheio de feitiços poderosos."

    grimorio.set_password("segredo123")

    if grimorio.check_password("segredo123"):
        print("Grimório aberto com sucesso!")
    else:
        print("Senha incorreta.")