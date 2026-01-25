
from src.models.state.reward_states import Reward
from src.utils.converters import orm_to_name_value
from typing import Any
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from profession import Profession
    from status import Attributes

class Activity:
    def __init__(self, name: str, baseXP:float, strain:list["Attributes"] | None): # adjust strain
        self._id: int=0
        self._name: str=name
        self._baseXP: float=baseXP
        self._activity_type: str = "other"
        self._strain: Any = [] if strain is None else strain
        self._compound_activity_links: Any =[]
        self._load:int=0
        
    
    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, new_load:int):
        self._load=new_load
      

    @property
    def id(self):
        return self._id
    
    @property
    def compound_activity_links(self):
        return self._compound_activity_links

    @compound_activity_links.setter
    def compound_activity_links(self, new_compound_activity_links:str):
        self._compound_activity_links=new_compound_activity_links
    
    @property
    def activity_type(self):
        return self._activity_type

    @activity_type.setter
    def activity_type(self, new_activity_type:str):
        self._activity_type=new_activity_type
    
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
    
    def perform(self):
        reward=Reward(xp=self.baseXP, ap=[], pp=[])
        reward.save_attributes(self.strain)
        return reward

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
    def __init__(self, name: str, xp:float, activities:list["Activity"] | None, profession_load: list["Profession"] | None):
        self._id: int=0
        self._name: str=name
        self._xp: float=xp
        self._activities: Any=[] if activities is None else activities
        self._profession_load: Any=[] if profession_load is None else profession_load
        self.load=0
        
    @property
    def load(self):
        return self._load
    
    @load.setter
    def load(self, load:int):
        self._load=load
        
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
    def xp(self):
        return self._xp

    @property
    def activities(self):
        return self._activities
    
    @property
    def professional_load(self):
        return self._profession_load
    
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