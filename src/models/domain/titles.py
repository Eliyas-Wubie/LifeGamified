from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.accomplishment import Accomplishment
class Title:
    def __init__(
            self,
            name:str,
            description:str|None = None,
            accomplishments:list["Accomplishment"]|None=None) -> None:
        self._id=0
        self._name=name
        self._description=description
        self._accomplishments= [] if accomplishments is None else accomplishments
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id:int):
        self._id=new_id
        
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def accomplishments(self):
        return self._accomplishments
    
    @accomplishments.setter
    def accomplishments(self, new_acc:list["Accomplishment"]):
        self._accomplishments=new_acc