from typing import  TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.status import Attribute
    from src.models.domain.profession import Profession
    from src.models.domain.titles import Title
    from src.models.domain.mission import Mission
    
class Accomplishment:
    def __init__(
            self, 
            name: str, 
            difficulty: int, 
            description: str,
            status: str | None = None,
            attributes:list["Attribute"] | None = None,    
            professions:list["Profession"] | None = None,
            titles:list["Title"] | None = None, 
            missions:list["Mission"] | None = None
        ):
        self._id: int=-1
        self._load: int=0
        self._name=name
        self._description= description
        self._status= "locked" if status is None else status
        self._difficulty=difficulty
        self._attributes= [] if attributes is None else attributes
        self._professions= [] if professions is None else professions
        self._titles= [] if titles is None else titles
        self._missions= [] if missions is None else missions

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, new_description:str):
        self._description = new_description
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status:str):
        self._status = new_status
        
    @property
    def load(self):
        return self._load
    
    @load.setter
    def load(self, new_load:int):
        self._load = new_load

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
    def professions(self, new_professions:list["Profession"]):
        self._professions = new_professions
    @property
    def missions(self):
        return self._missions 
    @missions.setter
    def missions(self, new_missions:list["Mission"]):
        self._missions = new_missions
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name:str):
        self._name = new_name
    @property
    def difficulty(self):
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, new_difficulty: int):
        self._difficulty = new_difficulty
    @property
    def attributes(self):
        return self._attributes
    @attributes.setter
    def attributes(self, new_attributes:list["Attribute"]):
        self._attributes = new_attributes
    @property
    def titles(self):
        return self._titles
    @titles.setter
    def titles(self, new_titles:list["Title"]):
        self._titles = new_titles

# accomplished is done on ORM so service should handle it manager not needed