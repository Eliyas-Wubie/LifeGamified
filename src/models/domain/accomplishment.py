from typing import Any
class Accomplishment:
    def __init__(self, name: str, difficulty: int, attributes:list[Any], professions:list[Any],titles:list[Any]):
        self._name=name
        self._difficulty=difficulty
        self._attributes=attributes
        self._professions=professions
        self._titles=titles
        # we need a mission link too
        self._id=0
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id:int):
        self._id = new_id

    @property
    def professions(self):
        return self._professions
    
    @professions.setter
    def professions(self, new_professions:int):
        self._professions = new_professions
        
    
    @property
    def name(self):
        return self._name
    @property
    def difficulty(self):
        return self._difficulty
    @property
    def attributes(self):
        return self._attributes
    @property
    def titles(self):
        return self._titles


class AccomplishmentManager:
    def __init__(self):
        pass