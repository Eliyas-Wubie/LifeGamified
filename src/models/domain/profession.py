from typing import Any
class Profession:
    def __init__(self, label:str, status:str, sub_professions: list[Any] | None=None):
        self._label=label
        self._status=status
        self._sub_profession=[] if sub_professions is None else sub_professions
    
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
    