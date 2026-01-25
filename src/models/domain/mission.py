
from typing import Any
from datetime import datetime

class Mission:
    def __init__(self, name:str, compound_activities:list[Any], deadline:datetime, bonus:dict[str,Any]):
        self._id=0
        self._name=name
        self._compound_activities=compound_activities
        self._deadline=deadline
        self._bonus=bonus
        self._load=datetime.now()
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id:int):
        self._id=id
    
    @property
    def load(self):
        return self._load
    
    @load.setter
    def load(self, new_load:int):
        self._load=new_load
        
    @property
    def name(self):
        return self._name
    
    @property
    def compound_activities(self):
        return self._compound_activities
    
    @property
    def deadline(self):
        return self._deadline
    
    @property
    def bonus(self):
        return self._bonus
    
    def execute(self):
        pass

class MissionManager:
    def __init__(self):
        pass