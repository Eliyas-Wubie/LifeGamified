from typing import Any
class Accomplishment:
    def __init__(self, name: str, difficulty: int, attributes:list[Any], professions:list[Any],reward_title:list[Any]):
        self._name=name
        self._difficulty=difficulty
        self._attribute_link=attributes
        self._profession_link=professions
        self._title_links=reward_title
        # we need a mission link too
        self._id=0
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id:int):
        self._id = new_id

    @property
    def profession_link(self):
        return self._profession_link
    
    @profession_link.setter
    def profession_link(self, new_profession_link:int):
        self._profession_link = new_profession_link
        
    
    @property
    def name(self):
        return self._name
    @property
    def difficulty(self):
        return self._difficulty
    @property
    def attribute_link(self):
        return self._attribute_link
    @property
    def title_links(self):
        return self._title_links


class AccomplishmentManager:
    def __init__(self):
        pass