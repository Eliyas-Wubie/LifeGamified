
from src.models.state.reward_states import Reward
from src.utils.converters import orm_to_name_value
from typing import Any
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from profession import Profession
    from status import Attributes

class BaseActivity:
    def __init__(self, name: str, xp:float, attributes:list["Attributes"] | None): # adjust attributes
        self._id: int=0
        self._name: str=name
        self._xp: float=xp
        self._activity_type: str = "other"
        self._attributes: Any = [] if attributes is None else attributes
        self._compound_activities: Any =[]
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
    def compound_activities(self):
        return self._compound_activities

    @compound_activities.setter
    def compound_activities(self, new_compound_activities:str):
        self._compound_activities=new_compound_activities
    
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
    def xp(self):
        return self._xp
    
    @property
    def attributes(self):
        return self._attributes
    
    def perform(self):
        reward=Reward(xp=self.xp, ap=[], pp=[])
        reward.save_attributes(self.attributes)
        return reward

class CompoundActivity:
    def __init__(self, name: str, xp:float, activities:list["BaseActivity"] | None, professions: list["Profession"] | None):
        self._id: int=0
        self._name: str=name
        self._xp: float=xp
        self._activities: Any=[] if activities is None else activities
        self._professions: Any=[] if professions is None else professions
        # missions link
        self._load=0
        
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
    def professions(self):
        return self._professions
    
    def perform(self):
        # calculate XP, AP, PP and return
        reward=Reward(xp=self.xp, ap=[], pp=[])
        reward.save_professions(orm_to_name_value(self.professions))
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