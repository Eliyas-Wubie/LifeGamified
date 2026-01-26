from typing import  TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.mission import Mission
    from src.models.domain.accomplishment import Accomplishment
    
    
class Profession:
    def __init__(
            self,
            name:str,
            status:str,
            parent: "Profession | None" = None,
            sub_professions: list["Profession"] | None=None,
            compound_activities: list["CompoundActivity"] | None=None,
            missions: list["Mission"] | None=None,
            accomplishments: list["Accomplishment"] | None=None,
            ):
        self._id: int = -1
        self._name = name
        self._status = status
        self._parent = parent
        self._sub_profession = [] if sub_professions is None else sub_professions
        self._compound_activities = [] if compound_activities is None else compound_activities
        self._missions = [] if missions is None else missions
        self._accomplishments = [] if accomplishments is None else accomplishments

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id:int):
        self._id=new_id   
    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, new_load:int):
        self._load=new_load
    
    @property
    def sub_profession(self):
        return self._sub_profession    
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, profession: "Profession | None"):
        self._parent = profession

    @property
    def compound_activities(self):
        return self._compound_activities
    @compound_activities.setter
    def compound_activities(self, compound_activities: list["CompoundActivity"]):
        self._compound_activities = compound_activities

    @property
    def missions(self):
        return self._missions
    @missions.setter
    def missions(self, missions: list["Mission"]):
        self._missions=missions
    
    @property
    def accomplishments(self):
        return self._accomplishments
    @accomplishments.setter
    def accomplishments(self, accomplishments: list["Accomplishment"]):
        self._accomplishments = accomplishments
    
    @property
    def name(self):
        return self._name
    
    @property
    def status(self):
        return self._status
    
    @property
    def sub_professions(self):
        return self._sub_profession

    def add_sub_profession(self, prof:"Profession"):
        self._sub_profession.append(prof)

    
    

class ProfessionManager:
    def __init__(self):
        pass
    