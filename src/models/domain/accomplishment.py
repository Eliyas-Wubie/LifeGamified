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
            attributes:list["Attribute"] | None = None,    
            professions:list["Profession"] | None = None,
            titles:list["Title"] | None = None, 
            missions:list["Mission"] | None = None
        ):
        self._id: int=-1
        self._load: int=0
        self._name=name
        # add description
        # add unlocked state
        self._difficulty=difficulty
        self._attributes= [] if attributes is None else attributes
        self._professions= [] if professions is None else professions
        self._titles= [] if titles is None else titles
        self._missions= [] if missions is None else missions

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

# accomplished is done on ORM so service should handle it manager not needed