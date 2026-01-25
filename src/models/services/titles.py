from src.models.db.models import TitlesORM
from src.models.domain.titles import Title
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def Title_orm_to_domain(orm: TitlesORM | None)->Title:
    from src.models.services.accomplishment import accomplishment_orm_to_domain
    
    accomplishments:Any = []
    if orm is None:
        return None # type: ignore
    for acc in orm.accomplishment_link:
        temp_domain=accomplishment_orm_to_domain(acc.accomplishments)    # handle by creating a new function in a different file?
        accomplishments.append(temp_domain)
    domain:Title = Title(orm.name, orm.description, accomplishments)
    domain.id=orm.id
    return domain

def Title_domain_to_orm(domain: Title) -> TitlesORM:
    Title:Any = session.query(TitlesORM).filter(TitlesORM.name == domain.name).first()
    return Title

def Title_create_orm_from_domain(domain: Title) -> TitlesORM:
    orm = TitlesORM(name=domain.name, description=domain.description)
    return orm
