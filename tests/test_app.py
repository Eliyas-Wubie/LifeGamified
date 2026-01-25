from src.models.domain.activity import BaseActivityClassFactory, Activity, CompoundActivity
from src.models.domain.profession import Profession # type: ignore
from src.models.domain.mission import Mission
from src.models.domain.status import Attributes
from src.models.domain.accomplishment import Accomplishment
from src.models.domain.titles import Title
from src.models.state.reward_states import Reward
from src.utils.config import load_config
from src.models.db.models import *
from src.models.services.activity import activity_create_orm_from_domain, activity_orm_to_domain, compound_activity_create_orm_from_domain
from src.models.services.status import attribute_domain_to_orm, attribute_create_orm_from_domain, attribute_orm_to_domain, attribute_domain_activity_population
from src.models.services.profession import  profession_create_orm_from_domain 
from src.models.services.mission import mission_create_orm_from_domain
from src.models.services.accomplishment import accomplishment_create_orm_from_domain
from src.models.services.titles import Title_create_orm_from_domain
from typing import Any
from datetime import datetime
from sqlalchemy.orm import joinedload

config=load_config()
class_list=[]
def test_base_activity_class_factory():
    global config, class_list
    dynamic_class_factory=BaseActivityClassFactory()
    def perform(self:Any)->Reward:
        reward=Reward(xp=self.baseXP, ap=self.strain, pp=[])
        return reward
  
    test_attrs={
        "perform":perform
    }
    class_list=[dynamic_class_factory.create_activity_class(base_activity, Activity, test_attrs) for base_activity in config.get("base_activities")]
    test_obj=class_list[0]("test", 12, None)
    assert len(class_list)>0
    assert isinstance(test_obj, Activity)
    assert isinstance(test_obj.perform(), Reward)
    assert test_obj.perform().xp == 12

def test_compound_activity():
    global config, class_list
    base_activities: list[Activity]=[BAclass("create", 1, {}) for BAclass in class_list]
    my_compound_obj=CompoundActivity( "dance", 112, base_activities, [])
    
    assert isinstance(my_compound_obj, CompoundActivity)
    assert my_compound_obj.name=="dance"
    assert my_compound_obj.activities==base_activities

def test_database():
    from src.models.db.session import SessionLocal
    
    session = SessionLocal() 
    

    act=Activity("dance", 12, None)
    attr=Attributes("abc", "mind", True)
    
    attr_orm=attribute_create_orm_from_domain(attr)
    session.add(attr_orm)
    act_orm=activity_create_orm_from_domain(act)
    session.add(act_orm)
    
    session.flush()
    
    assoc_orm=BaseActivityAttributesORM(base_activity_id=act_orm.id, attributes_id=attr_orm.id, rating=9)
    session.add(assoc_orm)
    session.commit()
    
    fetched_orm=session.query(BaseActivityORM).options(joinedload(BaseActivityORM.strain)).filter(BaseActivityORM.name=="dance").all()
    print("🚩🚩🚩🚩", fetched_orm)
    domain: Activity=activity_orm_to_domain(fetched_orm[-1])
    
    fetched_attribute=session.query(AttributesORM).options(
        joinedload(AttributesORM.contributor_activities)
        ).filter(AttributesORM.name=="abc").all()
    
    print("🌋🌋🌋🌋🌋👌👌",fetched_attribute[-1])
    orm_2: AttributesORM=attribute_domain_to_orm(attr)
    print("🌋🌋🌋🌋🌋👌👌",orm_2, orm_2.name, orm_2.area, orm_2.custom)
    domain_2: Attributes=attribute_orm_to_domain(fetched_attribute[-1])
    domain_2=attribute_domain_activity_population(domain_2, fetched_attribute[-1].contributor_activities)
    print("🌋🌋🌋🌋🌋👌👌",domain_2, domain_2.name, domain_2.area, domain_2.contributor_activities)
    
    print("🚩🚩🚩🚩", domain.strain[0].load)
    assert domain.name == "dance"
    assert domain.baseXP == 12
    assert isinstance(domain.strain,list)
    
    new_prof2=Profession("bus_driver", "begineer", None)
    new_prof=Profession("dirver", "begineer", [new_prof2])
    prof_orm=profession_create_orm_from_domain(new_prof)
    session.add(prof_orm)
    session.commit()
    
    fetched_profession=session.query(ProfessionORM).options(
        joinedload(ProfessionORM.parent)
        ).filter(ProfessionORM.label=="dirver").all()
    print("🚀🚀🚀🚀", fetched_profession[-1], fetched_profession[-1].label, fetched_profession[-1].status, fetched_profession[-1].sub_professions )
    assert isinstance(fetched_profession, list)
    
    base_activity_1=Activity("create", 77, None)
    base_activity_2=Activity("order", 57, None)
    # create the orms
    ba1_orm=activity_create_orm_from_domain(base_activity_1)
    ba2_orm=activity_create_orm_from_domain(base_activity_2)
    session.add(ba1_orm)
    session.add(ba2_orm)
    my_compound_obj=CompoundActivity( "draw", 112, [base_activity_1,base_activity_2], [])
    comp_orm=compound_activity_create_orm_from_domain(my_compound_obj)
    session.add(comp_orm)
    new_prof3=Profession("artist","advanced", None)
    prof3_orm=profession_create_orm_from_domain(new_prof3)
    session.add(prof3_orm)
    session.flush()
    # creating relation orms
    ba1_comp_orm=CompoundActivityBaseActivityORM(compound_activity_id=comp_orm.id, base_activity_id=ba1_orm.id, rating=5)
    ba2_comp_orm=CompoundActivityBaseActivityORM(compound_activity_id=comp_orm.id, base_activity_id=ba2_orm.id, rating=8)
    
    session.add(ba1_comp_orm)
    session.add(ba2_comp_orm)

    comp_prof_orm=CompoundActivityProfessionORM(profession_id=prof3_orm.id,compound_activity_id=comp_orm.id, rating=4 )
    session.add(comp_prof_orm)
    session.commit()
    
    fetched_profession2=session.query(ProfessionORM).options(
        joinedload(ProfessionORM.compound_activity_links)
        ).filter(ProfessionORM.label=="artist").all()
    print("🤣🤣🤣🤣", fetched_profession2[-1], fetched_profession2[-1].label, fetched_profession2[-1].status, fetched_profession2[-1].compound_activity_links[0].compound_activity.name )
    assert isinstance(fetched_profession2, list)
    
    #next handle mission and connect it back to profession
    mission1=Mission("run", [my_compound_obj],datetime.now(),{"brave":10, "solid":6})
    mission1_orm=mission_create_orm_from_domain(mission1)
    session.add(mission1_orm)
    session.flush()
    
    mission1_comp_orm=MissionCompoundActivityORM(
        mission_id=mission1_orm.id,
        compound_activity_id=comp_orm.id,
        rating=5
        )
    session.add(mission1_comp_orm)
    
    mission1_prof_orm=MissionProfessionORM(
        mission_id=mission1_orm.id,
        profession_id=prof3_orm.id,
        rating=5
    )
    session.add(mission1_prof_orm)
    
    session.commit()
    fetched_mission1=session.query(MissionsORM).options(
        joinedload(MissionsORM.compound_activities)
        ).filter(MissionsORM.name=="run").all()
    print("🌀🌀🐱‍🐉🐱‍🐉🌜", fetched_mission1[-1], fetched_mission1[-1].name, fetched_mission1[-1].bonus, fetched_mission1[-1].compound_activities[0].compound_activity.name )
    assert isinstance(fetched_mission1, list)
    fetched_mission2=session.query(MissionsORM).options(
        joinedload(MissionsORM.profession)
        ).filter(MissionsORM.name=="run").all()
    print("🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️", fetched_mission2[-1], fetched_mission2[-1].name, fetched_mission2[-1].deadline, fetched_mission2[-1].profession[0].profession.label )
    assert isinstance(fetched_mission2, list)
    
    # Accomplishment
    ac1=Accomplishment("win", 3, [], [], [])
    ac1_orm=accomplishment_create_orm_from_domain(ac1)
    
    session.add(ac1_orm)
    session.flush()
    ac1_attr_orm=AccomplishmentsAttributesORM(accomplishment_id=ac1_orm.id, attribute_id=orm_2.id, rating=3)
    session.add(ac1_attr_orm)
    session.commit()
    fetched_ac1=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.attribute_link)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac1[-1], fetched_ac1[-1].name, fetched_ac1[-1].difficulty, fetched_ac1[-1].attribute_link[0].attributes.name )
    assert isinstance(fetched_ac1, list)
    
    ac1_prof_orm=AccomplishmentsProfessionORM(accomplishment_id=ac1_orm.id, profession_id=prof3_orm.id, rating=6)
    session.add(ac1_prof_orm)
    session.commit()
    fetched_ac2=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.profession_link)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac2[-1], fetched_ac2[-1].name, fetched_ac2[-1].difficulty, fetched_ac2[-1].profession_link[0].professions.label )
    assert isinstance(fetched_ac2, list)
    
    title1=Title("honered one", "truely spacial")
    title1_orm=Title_create_orm_from_domain(title1)
    session.add(title1_orm)
    session.flush()
    
    ac1_title_orm=AccomplishmentsTitlesORM(accomplishment_id=ac1_orm.id, title_id=title1_orm.id)
    session.add(ac1_title_orm)
    
    session.commit()
    fetched_ac2=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.title_links)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac2[-1], fetched_ac2[-1].name, fetched_ac2[-1].difficulty, fetched_ac2[-1].title_links[0].titles.description )
    assert isinstance(fetched_ac2, list)
    
    ac1_mission_orm=MissionAccomplishmentORM(mission_id=mission1_orm.id, accomplishment_id=ac1_orm.id)
    session.add(ac1_mission_orm)
    session.commit()
    fetched_ac2=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.missions)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac2[-1], fetched_ac2[-1].name, fetched_ac2[-1].difficulty, fetched_ac2[-1].missions[0].mission.name )
    assert isinstance(fetched_ac2, list)
    
    
    session.commit()
    
    
    
    
    
    