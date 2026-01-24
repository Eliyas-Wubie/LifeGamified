
class Attributes:
    def __init__(self, name:str, area:str="", custom:bool=True):
        self._id=0
        self._name: str=name
        self._load: float=0
        self._area: str=area
        self._custom: bool=custom
        self._current_value: float=0
    
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
    