from typing import Any
class Profession:
    def __init__(self, name:str, status:str, sub_professions: list[Any] | None=None):
        self._name = name
        self._status = status
        self._sub_profession = [] if sub_professions is None else sub_professions
        self._parent = None
        self._compound_activities: list[Any] = []
        self._missions: list[Any] = []
        self._accomplishments: list[Any] = []
        self._load: int = 0
            
    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, new_load:int):
        self._load=new_load
    
    @property
    def sub_profession(self):
        return self._sub_profession
    @sub_profession.setter
    def sub_profession(self):
        return self._sub_profession
    
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self):
        return self._parent

    @property
    def compound_activities(self):
        return self._compound_activities
    @compound_activities.setter
    def compound_activities(self):
        return self._compound_activities

    @property
    def missions(self):
        return self._missions
    @missions.setter
    def missions(self):
        return self._missions
    
    @property
    def accomplishments(self):
        return self._accomplishments
    @accomplishments.setter
    def accomplishments(self):
        return self._accomplishments
    
    @property
    def name(self):
        return self._name
    
    @property
    def status(self):
        return self._status
    
    @property
    def sub_professions(self):
        return self._sub_profession

    def add_sub_profession(self, prof:Any):
        self._sub_profession.append(prof)
    def remove_sub_profession(self):
        pass
    
    

class ProfessionManager:
    def __init__(self):
        pass
    