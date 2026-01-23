
class Mission:
    def __init__(self, name, compound_activities, deadline, bonus):
        self._name=name
        self._compound_activities=compound_activities
        self._deadline=deadline
        self._bonus=bonus
        
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