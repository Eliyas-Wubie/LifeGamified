# perform a compound activity
from src.models.db.models import AttributesORM
from src.models.domain.status import Attributes
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def attribute_orm_to_domain(orm: AttributesORM)->Attributes:
    domain:Attributes = Attributes(name=orm.name)
    domain.id=orm.id
    return domain

def attribute_domain_to_orm(domain: Attributes) -> AttributesORM:
    attribute:Any = session.query(AttributesORM).filter(AttributesORM.name == domain.name).first()
    print(attribute)
    return attribute

def attribute_create_orm_from_domain(domain: Attributes) -> AttributesORM:
    orm = AttributesORM(name=domain.name, area=domain.area, custom=True, current_value=domain.current_value)
    return orm