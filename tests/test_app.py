from src.models.domain.activity import BaseActivity, CompoundActivity
from src.models.domain.profession import Profession
from src.models.domain.mission import Mission
from src.models.domain.status import Attribute
from src.models.domain.accomplishment import Accomplishment
from src.models.domain.titles import Title
from src.models.state.reward_states import Reward
from src.utils.config import load_config
from src.utils.class_factory import ClassFactory
from src.models.db.models import *
from src.models.services.activity import create_activity_orm, activity_orm_to_domain, create_compound_activity_orm
from src.models.services.status import attribute_domain_to_orm, create_attribute_orm, attribute_orm_to_domain, populate_base_activities
from src.models.services.profession import  create_profession_orm 
from src.models.services.mission import create_mission_orm
from src.models.services.accomplishment import create_accomplishment_orm
from src.models.services.title import create_title_orm
from src.models.state.accomplishment import AccomplishmentCache
from typing import Any
from datetime import datetime
from sqlalchemy.orm import joinedload

config=load_config()
class_list=[]
def test_base_activity_class_factory():
    global config, class_list
    dynamic_class_factory=ClassFactory()
    def perform(self:Any)->Reward:
        reward=Reward(xp=self.xp, ap=self.attributes, pp=[])
        return reward
  
    test_attrs={
        "perform":perform
    }
    class_list=[dynamic_class_factory.create_class(base_activity, BaseActivity, test_attrs) for base_activity in config.get("base_activities")]
    test_obj=class_list[0]("test", 12, None)
    assert len(class_list)>0
    assert isinstance(test_obj, BaseActivity)
    assert isinstance(test_obj.perform(), Reward)
    assert test_obj.perform().xp == 12

def test_compound_activity():
    global config, class_list
    base_activities: list[BaseActivity]=[BAclass("create", 1, {}) for BAclass in class_list]
    my_compound_obj=CompoundActivity( "dance", 112, [], base_activities, [], [])
    
    assert isinstance(my_compound_obj, CompoundActivity)
    assert my_compound_obj.name=="dance"
    assert my_compound_obj.activities==base_activities

def test_database():
    from src.models.db.session import SessionLocal
    
    session = SessionLocal() 
    

    act=BaseActivity("dance", 12)
    attr=Attribute("abc", "mind", True)
    
    attr_orm=create_attribute_orm(attr)
    session.add(attr_orm)
    act_orm=create_activity_orm(act)
    session.add(act_orm)
    
    session.flush()
    
    assoc_orm=BaseActivityAttributeORM(base_activity_id=act_orm.id, attributes_id=attr_orm.id, load=9)
    session.add(assoc_orm)
    session.commit()
    
    fetched_orm=session.query(BaseActivityORM).options(joinedload(BaseActivityORM.attributes)).filter(BaseActivityORM.name=="dance").all()
    print("🚩🚩🚩🚩", fetched_orm)
    domain: BaseActivity=activity_orm_to_domain(fetched_orm[-1])
    
    fetched_attribute=session.query(AttributeORM).options(
        joinedload(AttributeORM.base_activities)
        ).filter(AttributeORM.name=="abc").all()
    
    print("🌋🌋🌋🌋🌋👌👌",fetched_attribute[-1])
    orm_2: AttributeORM=attribute_domain_to_orm(attr)
    print("🌋🌋🌋🌋🌋👌👌",orm_2, orm_2.name, orm_2.area, orm_2.custom)
    domain_2: Attribute=attribute_orm_to_domain(fetched_attribute[-1])
    domain_2=populate_base_activities(domain_2, fetched_attribute[-1].base_activities)
    print("🌋🌋🌋🌋🌋👌👌",domain_2, domain_2.name, domain_2.area, domain_2.base_activities)
    
    print("🚩🚩🚩🚩", domain.attributes[0].load)
    assert domain.name == "dance"
    assert domain.xp == 12
    assert isinstance(domain.attributes,list)
    
    new_prof2=Profession("bus_driver", "begineer")
    new_prof=Profession("dirver", "begineer", sub_professions=[new_prof2])
    prof_orm=create_profession_orm(new_prof)
    session.add(prof_orm)
    session.commit()
    
    fetched_profession=session.query(ProfessionORM).options(
        joinedload(ProfessionORM.parent)
        ).filter(ProfessionORM.name=="dirver").all()
    print("🚀🚀🚀🚀", fetched_profession[-1], fetched_profession[-1].name, fetched_profession[-1].status, fetched_profession[-1].sub_professions )
    assert isinstance(fetched_profession, list)
    
    base_activity_1=BaseActivity("create", 77)
    base_activity_2=BaseActivity("order", 57)
    # create the orms
    ba1_orm=create_activity_orm(base_activity_1)
    ba2_orm=create_activity_orm(base_activity_2)
    session.add(ba1_orm)
    session.add(ba2_orm)
    my_compound_obj=CompoundActivity( "draw", 112, ["daily"],[base_activity_1,base_activity_2], [], [])
    comp_orm=create_compound_activity_orm(my_compound_obj)
    session.add(comp_orm)
    new_prof3=Profession("artist","advanced")
    prof3_orm=create_profession_orm(new_prof3)
    session.add(prof3_orm)
    session.flush()
    # creating relation orms
    ba1_comp_orm=BaseActivityCompoundActivityORM(compound_activity_id=comp_orm.id, base_activity_id=ba1_orm.id, load=5)
    ba2_comp_orm=BaseActivityCompoundActivityORM(compound_activity_id=comp_orm.id, base_activity_id=ba2_orm.id, load=8)
    
    session.add(ba1_comp_orm)
    session.add(ba2_comp_orm)

    comp_prof_orm=CompoundActivityProfessionORM(profession_id=prof3_orm.id,compound_activity_id=comp_orm.id, load=4 )
    session.add(comp_prof_orm)
    session.commit()
    
    fetched_profession2=session.query(ProfessionORM).options(
        joinedload(ProfessionORM.compound_activities)
        ).filter(ProfessionORM.name=="artist").all()
    print("🤣🤣🤣🤣", fetched_profession2[-1], fetched_profession2[-1].name, fetched_profession2[-1].status, fetched_profession2[-1].compound_activities[0].compound_activity.name )
    assert isinstance(fetched_profession2, list)
    
    #next handle mission and connect it back to profession
    mission1=Mission("run","descrippppption", datetime.now(), [{"name":"bravery", "type":"xp", "value":11}],[my_compound_obj],[],[])
    mission1_orm=create_mission_orm(mission1)
    session.add(mission1_orm)
    session.flush()
    
    mission1_comp_orm=CompoundActivityMissionORM(
        mission_id=mission1_orm.id,
        compound_activity_id=comp_orm.id,
        )
    session.add(mission1_comp_orm)
    
    mission1_prof_orm=MissionProfessionORM(
        mission_id=mission1_orm.id,
        profession_id=prof3_orm.id,
        load=5
    )
    session.add(mission1_prof_orm)
    
    session.commit()
    fetched_mission1=session.query(MissionORM).options(
        joinedload(MissionORM.compound_activities)
        ).filter(MissionORM.name=="run").all()
    print("🌀🌀🐱‍🐉🐱‍🐉🌜", fetched_mission1[-1], fetched_mission1[-1].name, fetched_mission1[-1].bonus, fetched_mission1[-1].compound_activities[0].compound_activity.name )
    assert isinstance(fetched_mission1, list)
    fetched_mission2=session.query(MissionORM).options(
        joinedload(MissionORM.professions)
        ).filter(MissionORM.name=="run").all()
    print("🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️🤷‍♂️", fetched_mission2[-1], fetched_mission2[-1].name, fetched_mission2[-1].deadline, fetched_mission2[-1].professions[0].profession.name )
    assert isinstance(fetched_mission2, list)
    
    # Accomplishment
    a_cache=AccomplishmentCache()
    ac1=Accomplishment("win", 3, [], [], [], [])
    ac1_orm=create_accomplishment_orm(ac1)
    a_cache.add_to_cache(ac1, ac1_orm)
    
    session.add(ac1_orm)
    session.flush()
    ac1_attr_orm=AccomplishmentAttributeORM(accomplishment_id=ac1_orm.id, attribute_id=orm_2.id, load=3)
    session.add(ac1_attr_orm)
    session.commit()
    fetched_ac1=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.attributes)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac1[-1], fetched_ac1[-1].name, fetched_ac1[-1].difficulty, fetched_ac1[-1].attributes[0].attribute.name )
    print("🚒🚒🚒", a_cache.query_domain_cache(ac1)==ac1)
    print("🚒🚒🚒", a_cache.query_orm_cache(ac1_orm)==ac1_orm)
    print("🚒🚒🚒", a_cache.query_inverse_cache(ac1_orm)==ac1)
    print("🚒🚒🚒", a_cache.query_inverse_cache(ac1)==ac1_orm)
    print("🚒🚒🚒", a_cache.query_inverse_cache(ac1)==ac1)
    ac_test1=Accomplishment("win", 3, [], [], [], [])
    ac_test2=Accomplishment("win", 3, [], [], [], [])
    
    a_cache.add_to_cache(ac_test1)
    a_cache.add_to_cache(ac_test2, ac1_orm)
    ac_test3=ac_test1
    print("🚒🚒🚒2", a_cache.query_domain_cache(ac_test1)==ac1)
    print("🚒🚒🚒2", a_cache.query_domain_cache(ac_test2)==ac1)
    print("🚒🚒🚒2", a_cache.query_domain_cache(ac_test2)==ac_test1)
    print("🚒🚒🚒2", a_cache.query_inverse_cache(ac_test2)==a_cache.query_inverse_cache(ac1)) # means duplicate orm already exists, should this be allowed?
    print("🚒🚒🚒2", a_cache.query_domain_cache(ac_test1)==ac_test3)
    
    
    
    
    
    
    
    
    
    
    
    assert isinstance(fetched_ac1, list)
    
    ac1_prof_orm=AccomplishmentProfessionORM(accomplishment_id=ac1_orm.id, profession_id=prof3_orm.id, load=6)
    session.add(ac1_prof_orm)
    session.commit()
    fetched_ac2=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.professions)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac2[-1], fetched_ac2[-1].name, fetched_ac2[-1].difficulty, fetched_ac2[-1].professions[0].profession.name )
    assert isinstance(fetched_ac2, list)
    
    title1=Title("honered one", "truely spacial")
    title1_orm=create_title_orm(title1)
    session.add(title1_orm)
    session.flush()
    
    ac1_title_orm=AccomplishmentTitleORM(accomplishment_id=ac1_orm.id, title_id=title1_orm.id)
    session.add(ac1_title_orm)
    
    session.commit()
    fetched_ac2=session.query(AccomplishmentORM).options(
        joinedload(AccomplishmentORM.titles)
        ).filter(AccomplishmentORM.name=="win").all()
    print("🎶🎶🎶🎶", fetched_ac2[-1], fetched_ac2[-1].name, fetched_ac2[-1].difficulty, fetched_ac2[-1].titles[0].title.description )
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
    
    
    
    
    
    