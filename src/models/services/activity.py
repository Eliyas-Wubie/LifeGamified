# create compound activity
# create a base actvity - sync/other
# perform a compound activity
from src.models.db.models import BaseActivityORM, CompoundActivityORM
from src.models.domain.activity import BaseActivity, CompoundActivity
from typing import Any
from src.models.db.session import SessionLocal

    
session = SessionLocal()

def activity_orm_to_domain(orm: BaseActivityORM | None)->BaseActivity:
    from src.models.services.status import attribute_orm_to_domain
    
    attributes:Any = []
    if orm is None:
        return None # type: ignore
    for association in orm.attributes:
        temp_domain=attribute_orm_to_domain(association.attribute)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        attributes.append(temp_domain)
    domain:BaseActivity = BaseActivity(orm.name, orm.xp, attributes)
    domain.id=orm.id
    domain.activity_type=orm.activity_type
    return domain

def activity_domain_to_orm(domain: BaseActivity) -> BaseActivityORM:
    activity:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
    return activity

def create_activity_orm(domain: BaseActivity) -> BaseActivityORM:
    orm = BaseActivityORM(name=domain.name, xp=domain.xp, activity_type="other")
    return orm

def compound_activity_orm_to_domain(orm: CompoundActivityORM | None)->CompoundActivity:
    from src.models.services.profession import profession_orm_to_domain
    
    activities:Any = []
    professions:Any=[]
    
    if orm is None:
        return None # type: ignore
    for b_act in orm.base_activities:
        temp_domain=activity_orm_to_domain(b_act.base_activity) 
        temp_domain.load=b_act.load
        activities.append(temp_domain)
    for prof in orm.professions:
        temp_domain=profession_orm_to_domain(prof.profession)
        temp_domain.load=prof.load
        professions.append(temp_domain)
    
    domain:CompoundActivity = CompoundActivity(orm.name, orm.xp, activities, professions)
    domain.id=orm.id
    return domain

def compound_activity_domain_to_orm(domain: CompoundActivity) -> CompoundActivityORM:
    c_activity:Any = session.query(CompoundActivityORM).filter(CompoundActivityORM.name == domain.name).first()
    return c_activity

def create_compound_activity_orm(domain: CompoundActivity) -> CompoundActivityORM:
    orm = CompoundActivityORM(name=domain.name, xp=domain.xp)
    return orm