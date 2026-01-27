from src.models.db.models import BaseActivityORM, CompoundActivityORM
from src.models.domain.activity import BaseActivity, CompoundActivity
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.domain.status import Attribute
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.activity import BaseActivity
    from src.models.domain.profession import Profession
    from src.models.domain.mission import Mission
    
        
        
session = SessionLocal()

def activity_orm_to_domain(orm: BaseActivityORM )->BaseActivity:
    from src.models.services.status import attribute_orm_to_domain
    
    attributes:list["Attribute"] = []
    compound_activities:list["CompoundActivity"]= []
    for association in orm.attributes:
        temp_domain=attribute_orm_to_domain(association.attribute)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        attributes.append(temp_domain)
    for association in orm.compound_activities:
        temp_domain=compound_activity_orm_to_domain(association.compound_activity)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        compound_activities.append(temp_domain)
    domain:BaseActivity = BaseActivity(orm.name, orm.xp, attributes=attributes)
    domain.id=orm.id
    domain.activity_type=orm.activity_type
    domain.compound_activities=compound_activities
    return domain

def activity_domain_to_orm(domain: BaseActivity) -> BaseActivityORM:
    activity:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
    return activity

def create_activity_orm(domain: BaseActivity) -> BaseActivityORM:
    orm = BaseActivityORM(name=domain.name, xp=domain.xp, activity_type="other")
    return orm


def compound_activity_orm_to_domain(orm: CompoundActivityORM )->CompoundActivity:
    from src.models.services.profession import profession_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain
    
    activities:list["BaseActivity"] = []
    professions:list["Profession"]=[]
    missions:list["Mission"]=[]

    
    for association in orm.base_activities:
        temp_domain=activity_orm_to_domain(association.base_activity) 
        temp_domain.load=association.load
        activities.append(temp_domain)
    for association in orm.professions:
        temp_domain=profession_orm_to_domain(association.profession)
        temp_domain.load=association.load
        professions.append(temp_domain)
    for association in orm.missions:
        temp_domain=mission_orm_to_domain(association.mission)
        missions.append(temp_domain)

    domain:CompoundActivity = CompoundActivity(orm.name, orm.xp, orm.tags, activities, professions, missions)
    domain.id=orm.id
    return domain

def compound_activity_domain_to_orm(domain: CompoundActivity) -> CompoundActivityORM:
    c_activity:Any = session.query(CompoundActivityORM).filter(CompoundActivityORM.name == domain.name).first()
    return c_activity

def create_compound_activity_orm(domain: CompoundActivity) -> CompoundActivityORM:
    orm = CompoundActivityORM(name=domain.name, xp=domain.xp)
    return orm