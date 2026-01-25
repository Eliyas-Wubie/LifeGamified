from typing import Any
class Title:
    def __init__(self, name:str, description:str, accomplishments:list[Any]|None=None) -> None:
        self._id=0
        self._name=name
        self._description=description
        self._accomplishment_links=accomplishments if accomplishments is not None else []
    
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
    def accomplishment_links(self):
        return self._accomplishment_links
    
    @accomplishment_links.setter
    def accomplishment_links(self, new_acc:list[Any]):
        self._accomplishment_links=new_acc