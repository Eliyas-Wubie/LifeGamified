from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.accomplishment import Accomplishment
    
class Title:
    def __init__(
            self,
            name:str,
            description:str|None = None,
            status: str | None = None,
            accomplishments:list["Accomplishment"]|None=None) -> None:
        title_policy=TitlePolicy()
        if not title_policy.is_valid_status("locked" if status is None else status):
            raise ValueError("invalid bonus")
        del title_policy
        self._id=0
        self._name=name
        self._description=description
        self._status= "locked" if status is None else status
        self._accomplishments= [] if accomplishments is None else accomplishments

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status:str):
        self._status = new_status
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @name.setter
    def name(self, new_name:str):
        self._name = new_name


    @description.setter
    def description(self, new_description:str | None):
        self._description = new_description
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id:int):
        self._id=new_id
        

    
    @property
    def accomplishments(self):
        return self._accomplishments
    
    @accomplishments.setter
    def accomplishments(self, new_acc:list["Accomplishment"]):
        self._accomplishments=new_acc

class TitlePolicy:
    def is_valid_status(self, status:str):
        from src.utils.config import load_config
        config=load_config()
        valid_status: list[str]=config.get("valid_status")
        return status in valid_status