from src.models.db.models import AccomplishmentORM
from src.models.domain.accomplishment import Accomplishment
from typing import Any
from src.models.db.session import SessionLocal

    
session = SessionLocal()

def accomplishment_orm_to_domain(orm: AccomplishmentORM | None)->Accomplishment:
    from src.models.services.status import attribute_orm_to_domain
    from src.models.services.profession import profession_orm_to_domain
    
    attributes:Any = []
    professions:Any =[]
    if orm is None:
        return None # type: ignore
    for attr in orm.attributes:
        temp_domain=attribute_orm_to_domain(attr.attribute)    # handle by creating a new function in a different file?
        temp_domain.load=attr.load
        attributes.append(temp_domain)
    for prof in orm.professions:
        temp_domain=profession_orm_to_domain(prof.profession)    # handle by creating a new function in a different file?
        temp_domain.load=prof.load
        professions.append(temp_domain)
    domain:Accomplishment = Accomplishment(orm.name, orm.difficulty, attributes, professions, [])
    domain.id=orm.id
    return domain

def accomplishment_domain_to_orm(domain: Accomplishment) -> AccomplishmentORM:
    Accomplishment:Any = session.query(AccomplishmentORM).filter(AccomplishmentORM.name == domain.name).first()
    return Accomplishment

def create_accomplishment_orm(domain: Accomplishment) -> AccomplishmentORM:
    orm = AccomplishmentORM(name=domain.name, difficulty=domain.difficulty)
    return orm
