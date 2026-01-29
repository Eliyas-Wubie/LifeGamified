
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
        mission_policy=MissionPolicy()
        if (
            mission_policy.is_valid_bonus([] if bonus is None else bonus) or
            mission_policy.is_valid_deadline(deadline)
        ):
            raise ValueError("invalid bonus or deadline")
        del mission_policy
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
    def description(self, description:str | None):
        self._description=description
        
    @property
    def professions(self):
        return self._professions
    
    @professions.setter
    def professions(self, professions:list["Profession"]):
        self._professions=professions

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
    def accomplishments(self):
        return self._accomplishments
    
    @accomplishments.setter
    def accomplishments(self, new_accomplishments:list["Accomplishment"]):
        self._accomplishments=new_accomplishments
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name:str):
        self._name = new_name
    
    @property
    def compound_activities(self):
        return self._compound_activities

    @compound_activities.setter
    def compound_activities(self, new_compound_activities:list["CompoundActivity"]):
        self._compound_activities = new_compound_activities
    
    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, new_deadline:datetime | None):
        self._deadline = new_deadline

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, new_bonus: list[dict[str, Any]]):
        self._bonus = new_bonus
    
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

class MissionPolicy:
    def is_valid_deadline(self, deadline:datetime | None):
        if deadline:
            return deadline > datetime.now()
        else:
            return True

    def is_valid_bonus(self, bonus_list:list[dict[str, Any]]):
        from src.utils.config import load_config
        config=load_config()
        valid_bonus = config.get("bonus")
        valid_keys = ["name", "type", "load"]
        for bonus in bonus_list:
            for key in valid_keys:
                if key not in list(bonus.keys()):
                    return False
            if bonus.get("name", "") not in valid_bonus:
                return False
        return True


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
        