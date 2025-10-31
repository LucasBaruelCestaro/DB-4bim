from typing import Optional, Annotated, Dict

class Feitico:
    def __init__(self):
        self._name: Optional[str] = None
        self._difficulty: Optional[int] = None
        self._ingredients: Dict[str, int] = []
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
        
        if len(parsed) > 50:
            raise ValueError("O nome do feitiço não pode ter mais de 50 caracteres.")

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
            raise TypeError("Os ingredientes devem ser um dicionário no formato {nome: quantidade}.")
        
        if not value:
            raise ValueError("O dicionário de ingredientes não pode estar vazio.")
        
        for name, qty in value.items():
            if not isinstance(name, str):
                raise TypeError("O nome de cada ingrediente deve ser uma string.")
            if not name.strip():
                raise ValueError("Os nomes dos ingredientes não podem ser vazios.")
            if len(name.strip()) < 2:
                raise ValueError(f"O nome do ingrediente '{name}' deve ter pelo menos 2 caracteres.")

            if not isinstance(qty, int):
                raise TypeError(f"A quantidade do ingrediente '{name}' deve ser um número inteiro.")
            if qty <= 0:
                raise ValueError(f"A quantidade do ingrediente '{name}' deve ser maior que zero.")
            if qty > 999:
                raise ValueError(f"A quantidade do ingrediente '{name}' é muito alta (>999).")
        
        lower_names = [n.lower().strip() for n in value.keys()]

        if len(lower_names) != len(set(lower_names)):
            raise ValueError("O dicionário contém nomes de ingredientes duplicados.")
        
        self._ingredients = {k.strip(): v for k, v in value.items()}

    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("A descrição do feitiço deve ser uma string.")
        
        if not value:
            raise ValueError("A descrição do feitiço não pode ser vazia.")
        
        if len(value.strip()) < 5:
            raise ValueError("A descrição do feitiço deve ter pelo menos 5 caracteres.")
        
        parsed = " ".join(value.strip().split())

        if len(parsed) > 300:
            raise ValueError("A descrição do feitiço deve ter no máximo 300 caracteres.")
        
        self._description = parsed

    @property
    def casting_time(self) -> Optional[Annotated[int, "Em segundos"]]:
        return self._casting_time
    
    @casting_time.setter
    def casting_time(self, value: Annotated[int, "Em segundos"]) -> None:
        if not isinstance(value, int):
            raise TypeError("O tempo de conjuração deve ser um número inteiro.")
        
        if value <= 0:
            raise ValueError("O tempo de conjuração deve ser maior que zero.")

        self._casting_time = value

    def to_dict(self) -> dict:
        return {k: v for k, v in {
            "name": self._name,
            "difficulty": self._difficulty,
            "ingredients": self._ingredients,
            "description": self._description,
            "casting_time": self._casting_time,
        }.items() if v is not None}