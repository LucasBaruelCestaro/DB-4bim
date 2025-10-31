from typing import Optional, Annotated, Dict, Union
import json
from cryptography.fernet import Fernet
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.crypto import derive_fernet_key_from_level

class Feitico:
    def __init__(self):
        self._name: Optional[str] = None
        self._difficulty: Optional[int] = None
        self._ingredients: Dict[str, int] = {}
        self._description: Optional[str] = None
        self._casting_time: Optional[Annotated[int, "Em segundos"]] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("O nome do feitiço deve ser uma string.")
        
        parsed = value.strip()

        if not parsed or len(parsed) < 3 or len(parsed) > 50:
            raise ValueError("O nome do feitiço deve ter entre 3 e 50 caracteres.")
        
        self._name = parsed

    @property
    def difficulty(self) -> Optional[int]:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("A dificuldade do feitiço deve ser um número inteiro.")
        
        if value < 1 or value > 10:
            raise ValueError("A dificuldade do feitiço deve estar entre 1 e 10.")
        
        self._difficulty = value

    @property
    def ingredients(self) -> Dict[str, int]:
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value: Dict[str, int]) -> None:
        if not isinstance(value, dict):
            raise TypeError("Os ingredientes devem ser um dicionário.")
        
        if not value:
            raise ValueError("Dicionário de ingredientes não pode estar vazio.")
        
        for k, v in value.items():
            if not isinstance(k, str) or not k.strip():
                raise ValueError(f"Nome de ingrediente inválido: {k}")
            
            if not isinstance(v, int) or v <= 0:
                raise ValueError(f"Quantidade inválida para {k}")
            
        self._ingredients = {k.strip(): v for k, v in value.items()}

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 5:
            raise ValueError("A descrição do feitiço deve ter pelo menos 5 caracteres.")
        
        self._description = " ".join(value.strip().split())

    @property
    def casting_time(self) -> Optional[Annotated[int, "Em segundos"]]:
        return self._casting_time

    @casting_time.setter
    def casting_time(self, value: Annotated[int, "Em segundos"]) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("O tempo de conjuração deve ser um inteiro > 0.")
        
        self._casting_time = value

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "name": self._name,
            "difficulty": self._difficulty,
            "ingredients": self._ingredients,
            "description": self._description,
            "casting_time": self._casting_time,
        }.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj._name = data.get("name")
        obj._difficulty = data.get("difficulty")
        obj._ingredients = data.get("ingredients", {})
        obj._description = data.get("description")
        obj._casting_time = data.get("casting_time")
        return obj

    def to_encrypted_dict_by_level(self, global_secret: str) -> dict:
        if self._difficulty is None:
            raise ValueError("Defina 'difficulty' antes de encriptar.")
        
        key = derive_fernet_key_from_level(global_secret, self._difficulty)
        f = Fernet(key)
        payload = json.dumps(self.to_dict()).encode("utf-8")
        encrypted = f.encrypt(payload).decode("utf-8")
        
        return {"level": self._difficulty, "encrypted": encrypted}

    @classmethod
    def from_encrypted_dict_by_mage_level(cls, data: dict, mage_level: int, global_secret: str):
        level = data.get("level")
        
        if level is None:
            raise ValueError("Dado criptografado inválido: 'level' ausente.")
        
        if mage_level < level:
            raise PermissionError(f"Nível do mago ({mage_level}) insuficiente para ver nível {level}.")
        
        encrypted = data.get("encrypted")

        if not encrypted:
            raise ValueError("Dado criptografado inválido: 'encrypted' ausente.")
        
        key = derive_fernet_key_from_level(global_secret, level)
        f = Fernet(key)
        decrypted = f.decrypt(encrypted.encode("utf-8"))
        payload = json.loads(decrypted.decode("utf-8"))

        return cls.from_dict(payload)
