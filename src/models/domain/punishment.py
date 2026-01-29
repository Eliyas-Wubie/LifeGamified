from abc import ABC, abstractmethod
from typing import Any

class Punishment(ABC):
    name: str
    punishment_type : str
    def __init__(self, punishment:Any) -> None:
        punishment_policy=PunishmentPolicy()
        if punishment_policy.is_valid_punishment(punishment):
            raise ValueError("invalid punishment")
        del punishment_policy
        self._punishment = punishment
        
    @property
    def punishment(self):
        return self._punishment
    @punishment.setter
    def punishment(self, new_punishment: Any):
        self._punishment = new_punishment
    
    @abstractmethod
    def get_punishment(self) -> dict[str,Any] | int:
        pass

class PunishmentPolicy:
    def is_valid_punishment(self, punishment:dict[str, Any]):
        from src.utils.config import load_config
        config=load_config()
        valid_punishment = config.get("punishment")
        valid_keys = ["name", "type", "load"]
        for key in valid_keys:
            if key not in list(punishment.keys()):
                return False
        if punishment.get("name", "") not in valid_punishment:
            return False
        return True
    