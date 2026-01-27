from typing import Any
from src.models.domain.profession import Profession
from src.models.domain.status import Attribute
from src.models.domain.accomplishment import Accomplishment
from src.models.domain.titles import Title
from src.models.domain.bonus import Bonus
from src.models.domain.punishment import Punishment

class Reward():
    def __init__(
            self,
            xp:float=0,
            ap:list[Attribute] | None = None,
            pp:list[Profession] | None = None,
            titles:list[Title] | None = None, 
            accomplishments:list[Accomplishment] | None = None
            ):
        self._xp = xp
        self._ap = ap if ap is not None else []
        self._pp = pp if pp is not None else []
        self._titles = titles if titles is not None else []
        self._accomplishments = accomplishments if accomplishments is not None else []
        
    @property
    def accomplishments(self):
        return self._accomplishments
    @accomplishments.setter
    def accomplishments(self, accomplishments: list[Accomplishment]):
        self._accomplishments = accomplishments

    @property
    def titles(self):
        return self._titles
    @titles.setter
    def titles(self, titles: list[Title]):
        self._titles = titles
    
    @property
    def xp(self)->float:
        return self._xp
    @property
    def ap(self):
        return self._ap
    @property
    def pp(self):
        return self._pp  
    @xp.setter
    def xp(self, xp: float):
        self._xp=xp
    @ap.setter
    def ap(self, ap: list[Attribute]):
        self._ap=ap
    @pp.setter
    def pp(self, pp: list[Profession]):
        self._pp=pp
    
    def extend_rewards(self, more_rewards: list[Any]):
        for reward in more_rewards:
            self.xp=self._xp + reward.xp
            self._ap.extend(reward.ap)
            self._pp.extend(reward.pp)
            # self.pp=self._pp + reward.pp
    
    def save_attributes(self, attributes_with_load: list[Any]):
        self._ap.extend(attributes_with_load)
    
    def save_professions(self, professions_With_load: list[Any]):
        self._pp.extend(professions_With_load)
    
    def apply_bonus(self, bonus:Bonus):
        bonus_item= bonus.get_bonus()
        if bonus.name == "xp" and isinstance(bonus_item, int):
            self.xp = self.xp + (100*bonus_item/10) # 100 is max 
        if  bonus.name == "ap" and isinstance(bonus_item, dict):
            for ap in self.ap:
                if ap.name == bonus_item.get("name"):
                    ap.load = ap.load + (3*bonus_item.get("value",1)/10) # 3 is max 
                    break
        if  bonus.name == "pp" and isinstance(bonus_item, dict):
            for pp in self.pp:
                if pp.name == bonus_item.get("name"):
                    pp.load = pp.load + (3*bonus_item.get("value",1)/10) # 3 is max 
                    break


    def apply_punishments(self, punishment:Punishment):
        punishment_item= punishment.get_punishment()
        if punishment.name == "xp" and isinstance(punishment_item, int):
            self.xp = self.xp + (100*punishment_item/10) # 100 is max 
        if  punishment.name == "ap" and isinstance(punishment_item, dict):
            for ap in self.ap:
                if ap.name == punishment_item.get("name"):
                    ap.load = ap.load + (3*punishment_item.get("value",1)/10) # 3 is max 
                    break
        if  punishment.name == "pp" and isinstance(punishment_item, dict):
            for pp in self.pp:
                if pp.name == punishment_item.get("name"):
                    pp.load = pp.load + (3*punishment_item.get("value",1)/10) # 3 is max 
                    break
    
    def get_dict(self):
        template: dict[str,float|list[Any]]={
            "xp":self.xp,
            "ap":self.ap,
            "pp":self.pp
        }
        return template
    