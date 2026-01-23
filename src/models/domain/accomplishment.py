class Accomplishment:
    def __init__(self, name, difficulty, required_attributes, reward_title):
        self._name=name
        self._difficulty=difficulty
        self._required_attribute=required_attributes
        self._reward_title=reward_title
        
    
    @property
    def name(self):
        return self._name
    @property
    def difficulty(self):
        return self._difficulty
    @property
    def required_attributes(self):
        return self._required_attribute
    @property
    def reward_title(self):
        return self._reward_title


class AccomplishmentManager:
    def __init__(self):
        pass