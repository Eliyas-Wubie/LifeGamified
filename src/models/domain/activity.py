
from abc import ABC, abstractmethod
from src.models.state.reward_states import Reward
from src.utils.converters import orm_to_name_value
from typing import Any
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from profession import Profession
    from status import Attributes

class Activity(ABC):
    def __init__(self, name: str, baseXP:float, strain:list["Attributes"] | None): # adjust strain
        self._id: int=0
        self._name: str=name
        self._baseXP: float=baseXP
        self._strain: Any = [] if strain is None else strain

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
    def baseXP(self):
        return self._baseXP
    
    @property
    def strain(self):
        return self._strain
    
    @abstractmethod
    def perform(self):
        pass

class BaseActivityClassFactory:
    _instance = None
    
    def __new__(cls, *args:Any, **kwargs:Any):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    
    def create_activity_class(self, class_name:str, base_class:Any, attrs:dict[str, Any]| None):
        if attrs is None:
            attrs={}
        
        def __init__(self:Any, *args:Any, **kwargs:Any):
            base_class.__init__(self, *args, **kwargs)
        
        attrs["__init__"] = __init__
        try:
            return type(class_name, (base_class,), attrs)
        
        except TypeError as e:
            raise TypeError(f"failed to create class {class_name} : {e}")

class CompoundActivity:
    def __init__(self, name: str, xp:float, activities:list["Activity"] | None, profession_load: list["Profession"] | None, accomplishment: list["Activity"] | None):
        self._id: int=0
        self._name: str=name
        self._xp: float=xp
        self._activities: Any=[] if activities is None else activities
        self._profession_load: Any=[] if profession_load is None else profession_load
        self._accomplishment: Any=[] if accomplishment is None else accomplishment
    
    @property
    def id(self):
        return self._id
    
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
        return self._profession_load
    
    @property
    def accomplishment(self):
        return self._accomplishment
    
    def perform(self):
        # calculate XP, AP, PP and return
        reward=Reward(xp=self.xp, ap=[], pp=[])
        reward.save_professions(orm_to_name_value(self.professional_load))
        reward.extend_rewards([activity.perform() for activity in self.activities])
        return reward
  
class ActivityManager: 
    _instance = None
    
    def __new__(cls, *arg: Any, **kwarg: Any):
        if cls._instance is None:
            return super().__new__(cls)
        return cls._instance

    def perform_activity(self, compound_activity: CompoundActivity):
        act_reward: Reward=compound_activity.perform()

        result:dict[str,float|dict[str,float]]={}
        result["xp"]=act_reward.xp
        result["ap"]=act_reward.ap
        result["pp"]=act_reward.pp
        
        return result
        
    def perform_activity_group(self, compound_activities: list[CompoundActivity]):
        collection:list[dict[str,float]]=[]
        for compound_activity in compound_activities:
            act_reward: Reward=compound_activity.perform()
            result:dict[str,float]={}
            result["xp"]=act_reward.xp
            result["ap"]=act_reward.ap
            result["pp"]=act_reward.pp
            collection.append(result)
            del act_reward
        return collection