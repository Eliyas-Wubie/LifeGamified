from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.activity import BaseActivity
class Attribute:
    def __init__(
            self,
            name:str,
            area:str,
            custom:bool=True,
            current_value: float=0,
            base_activities: list["BaseActivity"] | None = None
            ):
        self._id=-1
        self._load: int=0
        self._name=name
        self._area=area
        self._custom=custom
        self._current_value= current_value
        self._base_activities: list["BaseActivity"]=[] if base_activities is None else base_activities
    
    @property
    def base_activities(self):
        return self._base_activities
    
    @base_activities.setter
    def base_activities(self, new_list:list["BaseActivity"]):
        self._base_activities=new_list
    @property
    def custom(self):
        return self._custom
            
    @property
    def area(self):
        return self._area
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id:int):
        self._id=id
    
    @property
    def name(self):
        return self._name
    @property
    def load(self):
        return self._load
    @load.setter
    def load(self, load:int):
        self._load=load
    
    @property
    def current_value(self):
        return self._current_value
    @current_value.setter
    def current_value(self, current_value:int):
        self._current_value=current_value
        

    
# manager class here
    