from typing import List, Optional, Annotated

class Feitico:
    def __init__(self):
        self._name: Optional[str] = None
        self._difficulty: Optional[int] = None
        self._ingredients: List[str] = []
        self._description: Optional[str] = None
        self._casting_time: Optional[Annotated[int, "Em segundos"]] = None

    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("O nome do feitiço deve ser uma string.")

        if not value:
            raise ValueError("O nome do feitiço não pode ser vazio.")
        
        parsed = value.strip()

        if len(parsed) < 3:
            raise ValueError("O nome do feitiço deve ter pelo menos 3 caracteres.")

        self._name = parsed

    @property
    def difficulty(self) -> Optional[int]:
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, value: int) -> None:
        self._difficulty = value

    @property
    def ingredients(self) -> List[str]:
        return self._ingredients
    
    @ingredients.setter
    def ingredients(self, value: List[str]) -> None:
        self._ingredients = value

    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def casting_time(self) -> Optional[Annotated[int, "Em segundos"]]:
        return self._casting_time
    
    @casting_time.setter
    def casting_time(self, value: Annotated[int, "Em segundos"]) -> None:
        self._casting_time = value

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "difficulty": self._difficulty,
            "ingredients": self._ingredients,
            "description": self._description,
            "casting_time": self._casting_time,
        }
