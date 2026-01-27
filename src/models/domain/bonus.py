from abc import ABC, abstractmethod
from typing import Any

class Bonus(ABC):
    name: str
    bonus_type : str
    def __init__(self, bonus:Any) -> None:
        self._bonus=bonus
        
    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, new_bonus:Any):
        self._bonus=new_bonus
    
    @abstractmethod
    def get_bonus(self) -> dict[str,Any] | int:
        pass
    