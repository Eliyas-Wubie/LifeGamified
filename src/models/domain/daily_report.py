from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.mission import Mission
    

class DailyReport:
    def __init__(self, date:datetime, compound_activities:list["CompoundActivity"] | None = None, missions:list["Mission"] | None = None) -> None:
        
        self._id:int=-1
        self._date=date
        self._compound_activities=[] if compound_activities is None else compound_activities
        self._missions=[] if missions is None else missions

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, new_id:int):
        self._id = new_id
    
 
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, new_date:datetime):
        self._date = new_date
    
    @property
    def compound_activities(self):
        return self._compound_activities
    @compound_activities.setter
    def compound_activities(self, new_compound_activities:list["CompoundActivity"]):
        self._compound_activities = new_compound_activities
    @property
    def missions(self):
        return self._missions
    @missions.setter
    def missions(self, new_missions:list["Mission"]):
        self._missions = new_missions
        

class DailyReportPolicy:
    pass