
from typing import Any, TYPE_CHECKING
from datetime import datetime
from src.models.state.reward_states import Reward
from src.models.domain.bonus import Bonus
from src.models.domain.punishment import Punishment
from src.utils.class_factory import ClassFactory

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.accomplishment import Accomplishment
    from src.models.domain.profession import Profession
    
class Mission:
    def __init__(
            self,
            name:str,
            description: str | None = None, 
            deadline: datetime | None = None,
            bonus: list[dict[str,Any]] | None = None,  #[{name: bravery, type:xp, load:12}]
            compound_activities:list["CompoundActivity"] | None = None,
            accomplishments:list["Accomplishment"] | None = None,
            professions:list["Profession"] | None = None
            ):
        self._id: int = -1
        self._load: int = 0
        self._name=name
        self._description=description
        self._deadline=deadline
        self._bonus=[] if bonus is None else bonus
        self._compound_activities= [] if compound_activities is None else compound_activities
        self._accomplishments= [] if accomplishments is None else accomplishments
        self._professions= [] if professions is None else professions
        #  should i include prerequisite missions i.e profession like nested link - not on current version
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description:int):
        self._description=description

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id:int):
        self._id=id
    
    @property
    def load(self):
        return self._load
    
    @load.setter
    def load(self, new_load:int):
        self._load=new_load
        
    @property
    def name(self):
        return self._name
    
    @property
    def compound_activities(self):
        return self._compound_activities
    
    @property
    def deadline(self):
        return self._deadline
    
    @property
    def bonus(self):
        return self._bonus
    
    def execute(self):
        reward = Reward()
        for compound_activity in self.compound_activities:
            activity_reward = compound_activity.perform()
            reward.extend_rewards([activity_reward])
        for prof in self._professions:
            found=False
            for pp in reward.pp:
                if prof.name == pp.name:
                    pp.load=pp.load + prof.load
                    found=True
                    break
            if not found:
                reward.pp.append(prof)
        reward.accomplishments = self._accomplishments
        class_factory=ClassFactory()
        for bonus in self._bonus:
            attr: dict[str,Any]={}
            attr["bonus_type"]=bonus.get("bonus_type")
            attr["name"]=bonus.get("name")
            def get_bonus(self:Any):
                return self._bonus
            attr["get_bonus"]=get_bonus
            bonus_class=class_factory.create_class(bonus.get("name"),Bonus,attr)  # type: ignore
            reward.apply_bonus(bonus_class(bonus.get("value")))
        if self._deadline and self._deadline < datetime.now():
            punishment: dict[str, str|int]={
                "name": "deadline",
                "punishment_type":"xp",
                "value":10
            }
            attr: dict[str,Any]={}
            attr["bonus_type"]=punishment.get("punishment_type")
            attr["name"]=punishment.get("name")
            def get_punishment(self:Any):
                return self._punishment
            attr["get_punishment"]=get_punishment
            punishment_class=class_factory.create_class(punishment.get("name"),Punishment,attr)  # type: ignore
            reward.apply_punishments(punishment_class(punishment.get("value")))
        return reward

class MissionManager:
    _instance = None
    
    def __new__(cls, *arg: Any, **kwarg: Any):
        if cls._instance is None:
            return super().__new__(cls)
        return cls._instance
    def complete(self, mission:Mission):
        mission_reward : Reward= mission.execute()
        result:dict[str,Any]={}
        result["xp"]=mission_reward.xp
        
        result["ap"]={}
        for ap in mission_reward.ap:
            result.get("ap",{})[ap.name]=result.get("ap",{}).get(ap.name,0)+ap.load
            
        result["pp"]={}
        for pp in mission_reward.pp:
            result.get("pp",{})[pp.name]=result.get("pp",{}).get(pp.name,0)+pp.load
            
        return result
        