
from src.models.state.reward_states import Reward
from typing import Any
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.profession import Profession
    from src.models.domain.status import Attribute
    from src.models.domain.mission import Mission
    
class BaseActivity:
    def __init__(
            self, 
            name: str, 
            xp:float, 
            activity_type: str = "others",
            attributes:list["Attribute"] | None = None,
            compound_activities: list["CompoundActivity"] | None = None
            ): 
        base_activity_policy=ActivityPolicy()
        if not base_activity_policy.is_valid_activity_type(activity_type):
            raise ValueError("invalid activity type")
        del base_activity_policy
        self._id: int = -1
        self._load: int = 0
        self._name = name
        self._xp = xp
        self._activity_type = activity_type # name and type are usually the same except when it is other
        self._attributes= [] if attributes is None else attributes
        self._compound_activities = [] if compound_activities is None else compound_activities

        
    
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
    def compound_activities(self, new_compound_activities:list["CompoundActivity"]):
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
    
    @name.setter
    def name(self, new_name:str):
        self._name = new_name

    @xp.setter
    def xp(self, new_xp:float):
        self._xp =new_xp
    
    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, new_attributes:list["Attribute"]):
        self._attributes = new_attributes
    
    def perform(self):
        reward=Reward(xp=self.xp, ap=self._attributes, pp=[])
        return reward

class CompoundActivity:
    def __init__(
            self, 
            name: str, 
            xp:float, 
            tags:list[str] | None =None,
            activities:list["BaseActivity"] | None = None, 
            professions: list["Profession"] | None = None, 
            missions: list["Mission"] | None = None
        ):
        compound_activity_policy=ActivityPolicy()
        if not compound_activity_policy.is_valid_tag([] if tags is None else tags):
            raise ValueError("invalid tag")
        del compound_activity_policy
        self._id: int = -1
        self._load: int = 0
        self._name = name
        self._xp = xp
        self._tags = [] if tags is None else tags
        self._activities=[] if activities is None else activities
        self._professions=[] if professions is None else professions
        self._missions= [] if missions is None else missions
    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, tags:list[str]):
        self._tags=tags
        
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
    def missions(self):
        return self._missions
    @missions.setter
    def missions(self, missions:list["Mission"]):
        self._missions=missions
        
    @property
    def name(self):
        return self._name
    @property
    def xp(self):
        return self._xp
    
    @name.setter
    def name(self, new_name:str):
        self._name = new_name
    @xp.setter
    def xp(self, new_xp:float):
        self._xp = new_xp
    
    @property
    def activities(self):
        return self._activities
    @activities.setter
    def activities(self, new_activities: list["BaseActivity"]):
        self._activities = new_activities
    
    @property
    def professions(self):
        return self._professions
    @professions.setter
    def professions(self, new_professions:list["Profession"]):
        self._professions = new_professions

    def perform(self):
        reward=Reward(xp=self.xp, ap=[], pp=self._professions)
        reward.extend_rewards([activity.perform() for activity in self.activities])
        return reward

class ActivityPolicy:
    def is_valid_activity_type(self, activity_type:str):
        from src.utils.config import load_config
        config=load_config()
        valid_activities = config.get("base_activities")
        return activity_type in valid_activities
    
    def is_valid_tag(self, tags:list[str]):
        from src.utils.config import load_config
        config=load_config()
        valid_tags = config.get("valid_tags")
        for tag in tags:
            if tag not in valid_tags:
                return False
        return True
    
class ActivityManager: 
    _instance = None
    
    def __new__(cls, *arg: Any, **kwarg: Any):
        if cls._instance is None:
            return super().__new__(cls)
        return cls._instance

    def perform_activity(self, compound_activity: CompoundActivity):
        act_reward: Reward=compound_activity.perform()

        result:dict[str,Any]={}
        result["xp"]=act_reward.xp
        
        result["ap"]={}
        for ap in act_reward.ap:
            result.get("ap",{})[ap.name]=result.get("ap",{}).get(ap.name,0)+ap.load
            
        result["pp"]={}
        for pp in act_reward.pp:
            result.get("pp",{})[pp.name]=result.get("pp",{}).get(pp.name,0)+pp.load
            
        return result
        
    def perform_activity_group(self, compound_activities: list[CompoundActivity]):
        result: dict[str,Any]={}
        result["xp"]=0
        result["ap"] = {}
        result["pp"] = {}
        for compound_activity in compound_activities:
            act_reward: Reward=compound_activity.perform()

            result["xp"] = result.get("xp",0)+act_reward.xp
            for ap in act_reward.ap:
                result.get("ap",{})[ap.name]=result.get("ap",{}).get(ap.name,0)+ap.load
        
            for pp in act_reward.pp:
                result.get("pp",{})[pp.name]=result.get("pp",{}).get(pp.name,0)+pp.load
                
            del act_reward
        return result