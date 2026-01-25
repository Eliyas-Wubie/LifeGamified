# create compound activity
# create a base actvity - sync/other
# perform a compound activity
from src.models.db.models import BaseActivityORM, CompoundActivityORM
from src.models.domain.activity import Activity, CompoundActivity
from typing import Any
from src.models.db.session import SessionLocal

    
session = SessionLocal()

def activity_orm_to_domain(orm: BaseActivityORM | None)->Activity:
    from src.models.services.status import attribute_orm_to_domain
    
    strain:Any = []
    if orm is None:
        return None # type: ignore
    for association in orm.strain:
        temp_domain=attribute_orm_to_domain(association.attributes)    # handle by creating a new function in a different file?
        temp_domain.load=association.rating
        strain.append(temp_domain)
    domain:Activity = Activity(orm.name, orm.baseXP, strain)
    domain.id=orm.id
    domain.activity_type=orm.activity_type
    return domain

def activity_domain_to_orm(domain: Activity) -> BaseActivityORM:
    activity:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
    return activity

def activity_create_orm_from_domain(domain: Activity) -> BaseActivityORM:
    orm = BaseActivityORM(name=domain.name, baseXP=domain.baseXP, activity_type="other")
    return orm

def compound_activity_orm_to_domain(orm: CompoundActivityORM | None)->CompoundActivity:
    from src.models.services.profession import profession_orm_to_domain
    
    activities:Any = []
    professions:Any=[]
    
    if orm is None:
        return None # type: ignore
    for b_act in orm.base_activities_gage:
        temp_domain=activity_orm_to_domain(b_act.base_activity) 
        temp_domain.load=b_act.rating
        activities.append(temp_domain)
    for prof in orm.profession_links:
        temp_domain=profession_orm_to_domain(prof.profession)
        temp_domain.load=prof.rating
        professions.append(temp_domain)
    
    domain:CompoundActivity = CompoundActivity(orm.name, orm.xp, activities, professions)
    domain.id=orm.id
    return domain

def compound_activity_domain_to_orm(domain: CompoundActivity) -> CompoundActivityORM:
    c_activity:Any = session.query(CompoundActivityORM).filter(CompoundActivityORM.name == domain.name).first()
    return c_activity

def compound_activity_create_orm_from_domain(domain: CompoundActivity) -> CompoundActivityORM:
    orm = CompoundActivityORM(name=domain.name, xp=domain.xp)
    return orm