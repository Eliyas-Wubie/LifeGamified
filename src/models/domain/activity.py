from abc import ABC, abstractmethod

class Activity(ABC):
    def __init__(self,name: str, baseXP:int, strain:str):
        self._name=name
        self._baseXP=baseXP
        self._strain=strain
    
    @property
    def name(self):
        return self._name

    @property
    def baseXP(self):
        return self._baseXP
    
    @property
    def strain(self):
        return self._strain
    
    @abstractmethod
    def perform():
        pass

class BaseActivityClassFactory:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    
    def create_activity_class(self, class_name, base_class, attrs):
        if attrs is None:
            attrs={}
        
        def __init__(self, *args, **kwargs):
            base_class.__init__(self, *args, **kwargs)
        
        attrs["__init__"] = __init__
        try:
            return type(class_name, (base_class,), attrs)
        
        except TypeError as e:
            raise TypeError(f"failed to create class {class_name} : {e}")

class CompoundActivity:
    def __init__(self, name, xp, activities, profession_load, accomplishment):
        self._name=name
        self._xp=xp
        self._activities=activities
        self._profession_load=profession_load
        self._accomplishment=accomplishment
    
    @property
    def name(self):
        return self._name
    
    @property
    def xp(self):
        return self._xp

    @property
    def activities(self):
        return self._activities
    
    @property
    def professional_load(self):
        return self._professional_load
    
    @property
    def accomplishment(self):
        return self._accomplishment
    
    @abstractmethod
    def perform(self):
        pass

class ActivityManager:
    def __init__(self):
        pass