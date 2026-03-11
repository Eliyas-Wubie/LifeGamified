from src.models.domain.mission import Mission
from src.models.domain.activity import CompoundActivity
from src.models.domain.accomplishment import Accomplishment
from src.models.domain.daily_report import DailyReport
from src.models.domain.status import Attribute
from src.models.domain.profession import Profession
from src.models.services import activity as activity_service
from datetime import datetime

def get_missions():
    mission= Mission("name")
    mission2= Mission("name2")
    mission3= Mission("name3", "hahalu")
    mission4= Mission("name4")
    
    return [mission, mission2,mission3, mission4, mission, mission2,mission3, mission4, mission, mission2,mission3, mission4, mission, mission2,mission3, mission4, mission, mission2,mission3, mission4, mission, mission2,mission3, mission4 ]

def delete_mission(item):
    pass
def create_mission(data):
    pass
def delete_compound_activity(item):
    pass
def create_compound_activity(data):
    pass
def get_attributes():
    a1=Attribute("positivity", "mind")
    a2=Attribute("activeness", "mind")
    a3=Attribute("courage", "spirit")
    a4=Attribute("clarity", "spirit")
    a5=Attribute("strategy", "body")
    return [a1,a2,a3,a4,a5]

def get_professions():
    p1=Profession("dancer", "locked")
    p2=Profession("singer", "locked")
    p3=Profession("cartographer","locked", parent=p1)
    p4=Profession("voice coach", "locked",parent=p2)
    p5=Profession("opera", "locked",parent=p2)
    p6=Profession("lala", "locked",parent=p5)
    p7=Profession("kaka", "locked",parent=p5)
    p8=Profession("susu", "locked",parent=p6)
    p9=Profession("lala", "locked",parent=p4)
    p10=Profession("kaka", "locked",parent=p4)
    p11=Profession("susu", "locked",parent=p9)
    
    
    return [p1,p2,p3,p4,p5,p6, p7, p8, p9,p10, p11]

def get_compound_activities():
    return activity_service.view_compound_activities()


def get_daily_reports():
    # include accomplishment for each daily report as well as statistical info like xp, ap, pp gained 
    # compound activities completed missions completed and accomplishment acquired
    
    a= CompoundActivity("name3", 1, ["daily", "generic", "uncomfortable"])
    b= CompoundActivity("name4", 7)
    compound_activity= DailyReport(datetime.now(), compound_activities=[a,b])
    compound_activity2= DailyReport(datetime.now())
    compound_activity3= DailyReport(datetime.now())
    compound_activity4= DailyReport(datetime.now())
    return [compound_activity, compound_activity2, compound_activity3, compound_activity4]
def get_daily_activities():
    compoundActivity= CompoundActivity("name", 10)
    compoundActivity2= CompoundActivity("name2", 10)
    compoundActivity3= CompoundActivity("name3", 10)
    compoundActivity4= CompoundActivity("name4", 10)
    return [compoundActivity, compoundActivity2,compoundActivity3, compoundActivity4 ]
def get_uncomfortable_activities():
    compoundActivity= CompoundActivity("name", 10)
    compoundActivity2= CompoundActivity("name2", 10)
    compoundActivity3= CompoundActivity("name3", 10)
    compoundActivity4= CompoundActivity("name4", 10)
    return [compoundActivity, compoundActivity2,compoundActivity3, compoundActivity4 ]
def get_generic_activities():
    compoundActivity= CompoundActivity("name", 10)
    compoundActivity2= CompoundActivity("name2", 10)
    compoundActivity3= CompoundActivity("name3", 10)
    compoundActivity4= CompoundActivity("name4", 10)
    return [compoundActivity, compoundActivity2,compoundActivity3, compoundActivity4 ]
def get_accomplishments():
    accomplishment= Accomplishment("name", 5, "disc")
    accomplishment2= Accomplishment("name2", 5, "disc")
    accomplishment3= Accomplishment("name3", 5, "disc")
    accomplishment4= Accomplishment("name4", 5, "disc")
    return [accomplishment, accomplishment2,accomplishment3, accomplishment4 ]

def make_a_report(data):    pass
