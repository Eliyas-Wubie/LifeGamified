# perform a compound activity
from src.models.db.models import AttributeORM
from src.models.domain.status import Attributes
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def attribute_orm_to_domain(orm: AttributeORM)->Attributes:
    
    domain:Attributes = Attributes(name=orm.name, area=orm.area, custom=orm.custom)
    domain.id=orm.id
    domain.current_value=orm.current_value
    
    # for act in orm.base_activities:
    #     temp_domain=activity_orm_to_domain(act.base_activity)
    #     temp_domain.load=act.load
    #     domain.base_activities.append(temp_domain)
        
    return domain

def attribute_domain_to_orm(domain: Attributes) -> AttributeORM:
    attribute:Any = session.query(AttributeORM).filter(AttributeORM.name == domain.name).first()
    return attribute

def attribute_create_orm_from_domain(domain: Attributes) -> AttributeORM:
    orm = AttributeORM(name=domain.name, area=domain.area, custom=True, current_value=domain.current_value)
    return orm

def create_attribute_orm(domain:Attributes, act_orms:list[Any]):
    from src.models.services.activity import activity_orm_to_domain
    for act in act_orms:
        temp_domain=activity_orm_to_domain(act.base_activity)
        temp_domain.load=act.load
        domain.base_activities.append(temp_domain)
    return domain