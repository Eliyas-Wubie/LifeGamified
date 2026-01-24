from typing import Any
class Reward():
    def __init__(self, xp:float=0, ap:list[Any]=[], pp:list[Any]=[]):
        self._xp: float = xp
        self._ap: Any = ap
        self._pp: Any = pp
    
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
    def ap(self, ap: Any):
        self._ap=ap
    @pp.setter
    def pp(self, pp: Any):
        self._pp=pp
    
    def extend_rewards(self, more_rewards: list[Any]):
        for reward in more_rewards:
            self.xp=self._xp + reward.xp
            self.ap=self.save_attributes(reward.ap) #[{name:load}]
            self.pp=self.save_professions(reward.pp)
            # self.pp=self._pp + reward.pp
    def save_attributes(self, attributes_with_load: list[Any]):
        for attr in attributes_with_load:
            self.ap[attr.get("name")]=self.ap.get(attr.get("name"),0)+attr.get("load")
    def save_professions(self, professions_With_load: list[Any]):
        for prof in professions_With_load:
            self.ap[prof.get("name")]=self.ap.get(prof.get("name"),0)+prof.get("load")
    
    def get_dict(self):
        template: dict[str,float|list[Any]]={
            "xp":self.xp,
            "ap":self.ap,
            "pp":self.pp
        }
        return template
    