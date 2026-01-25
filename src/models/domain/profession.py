from typing import Any
class Profession:
    def __init__(self, label:str, status:str, sub_professions: list[Any] | None=None):
        self._label=label
        self._status=status
        self._sub_profession=[] if sub_professions is None else sub_professions
        self._parent=None
        self._compound_activity_links: list[Any]=[]
        self._mission_links: list[Any]=[]
        self._accomplishments_links: list[Any]=[]
        self._load:int=0
        
    
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
    def compound_activity_links(self):
        return self._compound_activity_links
    @compound_activity_links.setter
    def compound_activity_links(self):
        return self._compound_activity_links

    @property
    def mission_links(self):
        return self._mission_links
    @mission_links.setter
    def mission_links(self):
        return self._mission_links
    
    @property
    def accomplishments_links(self):
        return self._accomplishments_links
    @accomplishments_links.setter
    def accomplishments_links(self):
        return self._accomplishments_links
    
    @property
    def label(self):
        return self._label
    
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
    