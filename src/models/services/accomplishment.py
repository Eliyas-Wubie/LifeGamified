from src.models.db.models import AccomplishmentORM
from src.models.domain.accomplishment import Accomplishment
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.domain.status import Attribute
    from src.models.domain.profession import Profession
    from src.models.domain.titles import Title
    from src.models.domain.mission import Mission


    
session = SessionLocal()

def accomplishment_orm_to_domain(orm: AccomplishmentORM )->Accomplishment:
    from src.models.services.status import attribute_orm_to_domain
    from src.models.services.profession import profession_orm_to_domain
    from models.services.title import title_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain
    
    attributes:list["Attribute"] = []
    professions:list["Profession"] =[]
    titles:list["Title"]= []
    missions:list["Mission"]= []
    for association in orm.attributes:
        temp_domain=attribute_orm_to_domain(association.attribute)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        attributes.append(temp_domain)
    for association in orm.professions:
        temp_domain=profession_orm_to_domain(association.profession)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        professions.append(temp_domain)
    for association in orm.titles:
        temp_domain = title_orm_to_domain(association.title)
        titles.append(temp_domain)
    for association in orm.missions:
        temp_domain = mission_orm_to_domain(association.mission)
        missions.append(temp_domain)
    
        
    domain:Accomplishment = Accomplishment(orm.name, orm.difficulty, attributes, professions,titles,missions)
    domain.id=orm.id
    return domain

def accomplishment_domain_to_orm(domain: Accomplishment) -> AccomplishmentORM:
    Accomplishment:Any = session.query(AccomplishmentORM).filter(AccomplishmentORM.name == domain.name).first()
    return Accomplishment

def create_accomplishment_orm(domain: Accomplishment) -> AccomplishmentORM:
    orm = AccomplishmentORM(name=domain.name, difficulty=domain.difficulty)
    return orm
