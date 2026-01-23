class Profession:
    def __init__(self, label, status, sub_professions):
        self._label=label
        self._status=status
        self._sub_profession=sub_professions
    
    @property
    def label(self):
        return self._label
    
    @property
    def status(self):
        return self._status
    
    @property
    def sub_professions(self):
        return self._sub_profession

    def add_sub_profession(self):
        pass
    def remove_sub_profession(self):
        pass
    
    

class ProfessionManager:
    def __init__(self):
        pass
    