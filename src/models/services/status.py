# perform a compound activity
from src.models.db.models import AttributeORM
from src.models.domain.status import Attribute
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.db.models import BaseActivityAttributeORM
    
session = SessionLocal()

def attribute_orm_to_domain(orm: AttributeORM)->Attribute:
    domain:Attribute = Attribute(name=orm.name, area=orm.area, custom=orm.custom)
    domain.id=orm.id
    domain.current_value=orm.current_value
    
    return domain

def attribute_domain_to_orm(domain: Attribute) -> AttributeORM:
    attribute:Any = session.query(AttributeORM).filter(AttributeORM.name == domain.name).first()
    return attribute

def create_attribute_orm(domain: Attribute) -> AttributeORM:
    orm = AttributeORM(name=domain.name, area=domain.area, custom=True, current_value=domain.current_value)
    return orm

def populate_base_activities(domain:Attribute, act_orms:list["BaseActivityAttributeORM"]):
    from src.models.services.activity import activity_orm_to_domain
    for act in act_orms:
        temp_domain=activity_orm_to_domain(act.base_activity)
        temp_domain.load=act.load
        domain.base_activities.append(temp_domain)
    return domain