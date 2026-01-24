from src.models.domain.activity import BaseActivityClassFactory, Activity, CompoundActivity
from src.models.domain.status import Attributes
from src.models.state.reward_states import Reward
from src.utils.config import load_config
from src.models.db.models import *
from src.models.services.activity import activity_create_orm_from_domain, activity_orm_to_domain
from src.models.services.status import attribute_domain_to_orm, attribute_create_orm_from_domain
from typing import Any
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
    my_compound_obj=CompoundActivity( "dance", 112, base_activities, {}, [])
    
    assert isinstance(my_compound_obj, CompoundActivity)
    assert my_compound_obj.name=="dance"
    assert my_compound_obj.activities==base_activities

def test_database():
    from src.models.db.session import SessionLocal
    
    session = SessionLocal()
    
    tasks:Any = session.query(BaseActivityORM).all()
    for t in tasks:
        print(t.id, t.name)
    
    test_obj=class_list[0]("test", 12, {})
    attr=Attributes("abc", "mind", True)
    attr_orm=attribute_create_orm_from_domain(attr)
    session.add(attr_orm)
    session.flush()
    act_orm=activity_create_orm_from_domain(test_obj)
    session.add(act_orm)
    session.flush()
    print("🤳🤳🤳🤳", attr_orm.id)
    assoc_orm=BaseActivityAttributesORM(base_activity_id=act_orm.id, attributes_id=attr_orm.id, rating=9)
    session.add(assoc_orm)
    session.commit()
    
    fetched_orm=session.query(BaseActivityORM).options(joinedload(BaseActivityORM.strain)).filter(BaseActivityORM.name=="test").all()
    print("🚩🚩🚩🚩", fetched_orm)
    
    domain: Activity=activity_orm_to_domain(fetched_orm[-1], class_list[0])
    
    print("🚩🚩🚩🚩", domain.strain[0].load)
    assert domain.name =="test"
    assert domain.baseXP == 12
    assert isinstance(domain.strain,list)
    