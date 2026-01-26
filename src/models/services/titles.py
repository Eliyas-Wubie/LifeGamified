from src.models.db.models import TitleORM
from src.models.domain.titles import Title
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def Title_orm_to_domain(orm: TitleORM | None)->Title:
    from src.models.services.accomplishment import accomplishment_orm_to_domain
    
    accomplishments:Any = []
    if orm is None:
        return None # type: ignore
    for acc in orm.accomplishments:
        temp_domain=accomplishment_orm_to_domain(acc.accomplishment)    # handle by creating a new function in a different file?
        accomplishments.append(temp_domain)
    domain:Title = Title(orm.name, orm.description, accomplishments)
    domain.id=orm.id
    return domain

def Title_domain_to_orm(domain: Title) -> TitleORM:
    Title:Any = session.query(TitleORM).filter(TitleORM.name == domain.name).first()
    return Title

def create_title_orm(domain: Title) -> TitleORM:
    orm = TitleORM(name=domain.name, description=domain.description)
    return orm
