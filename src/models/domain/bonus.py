from abc import ABC, abstractmethod
from typing import Any

class Bonus(ABC):
    name: str
    bonus_type : str
    def __init__(self, bonus:Any) -> None:
        bonus_policy=BonusPolicy()
        if not bonus_policy.is_valid_bonus(bonus):
            raise ValueError("invalid bonus")
        del bonus_policy
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

class BonusPolicy:
    def is_valid_bonus(self, bonus:dict[str, Any]):
        from src.utils.config import load_config
        config=load_config()
        valid_bonus = config.get("bonus")
        valid_keys = ["name", "type", "load"]
        for key in valid_keys:
            if key not in list(bonus.keys()):
                return False
        if bonus.get("name", "") not in valid_bonus:
            return False
        return True
    