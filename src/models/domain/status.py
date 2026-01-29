from typing import TYPE_CHECKING, Any
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
        attribute_policy=AttributePolicy()
        if attribute_policy.is_valid_area(area):
            raise ValueError("invalid area")
        del attribute_policy
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

    @custom.setter
    def custom(self, new_custom: bool):
        self._custom = new_custom
   
    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, new_area:str):
        self._area = new_area
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id:int):
        self._id=id
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name:str):
        self._name = new_name
    
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
    def current_value(self, current_value:float):
        self._current_value=current_value

class AttributePolicy:
    def is_valid_area(self, area:str):
        from src.utils.config import load_config
        config=load_config()
        valid_areas = config.get("areas")
        return area in valid_areas
     
class Status: # singleton
    _instance = None
    
    def __new__(cls, *args: Any, **kwargs:Any): # but this dose not work on persistent instance i.e only one row
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance    
    
    def __init__(self, xp:float=0, level:int=0, attributes:list[Any] | None = None, titles:list[Any] | None = None) -> None:
        self._id = -1
        self._xp=xp
        self._level=level
        self._attributes=attributes
        self._titles=titles
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id:float):
        self._id = new_id

    @property
    def xp(self):
        return self._xp
    
    @xp.setter
    def xp(self, new_xp:float):
        self._xp = new_xp

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, new_level:int):
        self._level = new_level

    @property
    def attributes(self):
        return self._attributes
    
    @attributes.setter
    def attributes(self, new_attributes:int):
        self._attributes = new_attributes

    @property
    def titles(self):
        return self._titles
    
    @titles.setter
    def titles(self, new_titles:int):
        self._titles = new_titles



    