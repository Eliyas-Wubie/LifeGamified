from abc import ABC, abstractmethod
from typing import Any

class Punishment(ABC):
    name: str
    punishment_type : str
    def __init__(self, punishment:Any) -> None:
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
    