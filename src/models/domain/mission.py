
from typing import Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.accomplishment import Accomplishment
    from src.models.domain.profession import Profession
    

class Mission:
    def __init__(
            self,
            name:str,
            description: str | None = None, 
            deadline: datetime | None = None,
            bonus: dict[str,Any] | None = None, 
            compound_activities:list["CompoundActivity"] | None = None,
            accomplishments:list["Accomplishment"] | None = None,
            professions:list["Profession"] | None = None
            ):
        self._id: int = -1
        self._load: int = 0
        self._name=name
        self._description=description
        self._deadline=deadline
        self._bonus=bonus
        self._compound_activities= [] if compound_activities is None else compound_activities
        self._accomplishments= [] if accomplishments is None else accomplishments
        self._professions= [] if professions is None else professions
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description:int):
        self._description=description

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