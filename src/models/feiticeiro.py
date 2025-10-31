from typing import Optional

class Feiticeiro:
    def __init__(self):
        self.name: Optional[str] = None
        self.level: Optional[int] = None

    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("O nome do feiticeiro deve ser uma string.")

        parsed = value.strip()

        if not parsed or len(parsed) < 3 or len(parsed) > 50:
            raise ValueError("O nome do feiticeiro deve ter entre 3 e 50 caracteres.")
        
        self._name = parsed

    @property
    def level(self) -> Optional[int]:
        return self._level
    
    @level.setter
    def level(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("O nível do feiticeiro deve ser um número inteiro.")
        
        if value < 1 or value > 10:
            raise ValueError("O nível do feiticeiro deve estar entre 1 e 10.")
        
        self._level = value

    def to_dict(self) -> dict:
        data = {
            "name": self._name,
            "level": self._level,
        }
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Feiticeiro":
        obj = cls()
        obj._name = data.get("name")
        obj._level = data.get("level")
        
        return obj