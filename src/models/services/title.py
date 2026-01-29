from src.models.db.models import TitleORM
from src.models.domain.titles import Title
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal
from sqlalchemy import or_, and_

if TYPE_CHECKING:
    from src.models.domain.accomplishment import Accomplishment

# view titles,search and filter owned and unowned titles
# create title
# update title
# delete title

session = SessionLocal()

def title_orm_to_domain(orm: TitleORM )->Title:
    from src.models.services.accomplishment import accomplishment_orm_to_domain
    
    accomplishments:Any = []

    for association in orm.accomplishments:
        temp_domain=accomplishment_orm_to_domain(association.accomplishment)    # handle by creating a new function in a different file?
        accomplishments.append(temp_domain)
    domain:Title = Title(orm.name, orm.description, accomplishments)
    domain.id=orm.id
    return domain

def title_domain_to_orm(domain: Title) -> TitleORM:
    Title:Any = session.query(TitleORM).filter(TitleORM.name == domain.name).first()
    return Title

def create_title_orm(domain: Title) -> TitleORM:
    orm = TitleORM(name=domain.name, description=domain.description)
    return orm

#______________________________________________________________________________#
def view_owned_titles(search:str | None=None) -> list[Title]:
    if not search:
        titles:Any = session.query(TitleORM).filter(TitleORM.status == "unlocked").all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles
    else:
        titles:Any = session.query(TitleORM).filter(
            TitleORM.status == "unlocked").filter(
                or_(
                TitleORM.name.ilike(f"%{search}%"),
                TitleORM.description.ilike(f"%{search}%")
        )).all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles

def view_unowned_titles(search:str | None=None) -> list[Title]:
    if not search:
        titles:Any = session.query(TitleORM).filter(TitleORM.status == "locked").all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles
    else:
        titles:Any = session.query(TitleORM).filter(
            TitleORM.status == "locked").filter(
                or_(
                TitleORM.name.ilike(f"%{search}%"),
                TitleORM.description.ilike(f"%{search}%")
        )).all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles

def view_titles(search:str | None=None) -> list[Title]:
    if not search:
        titles:Any = session.query(TitleORM).all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles
    else:
        titles:Any = session.query(TitleORM).filter(
                or_(
                TitleORM.name.ilike(f"%{search}%"),
                TitleORM.description.ilike(f"%{search}%")
        )).all()
        domain_titles = [title_orm_to_domain(orm) for orm in titles] 
        return domain_titles

def update_title(
        domain:Title,
        new_name: str | None = None, 
        new_description:str | None = None,
        new_status: str | None = None
        ) ->Title:
    orm:TitleORM  = title_domain_to_orm(domain)
    if not orm:
        orm: TitleORM = create_title_orm(domain)

    orm.name = new_name if new_name is not None else orm.name
    domain.name = new_name if new_name is not None else domain.name
    
    orm.description = new_description if new_description is not None else orm.description
    domain.description = new_description if new_description is not None else domain.description
    
    orm.status = new_status if new_status is not None else orm.status
    domain.status = new_status if new_status is not None else domain.status
    session.commit()
    
    return domain

def control_title_accomplishment_link(control:str, domain:Title, accomplishment: "Accomplishment"):
    from src.models.services.accomplishment import accomplishment_domain_to_orm
    from src.models.db.models import AccomplishmentTitleORM
    if control == "link":
        title_orm=title_domain_to_orm(domain)
        accomplishment_orm=accomplishment_domain_to_orm(accomplishment)
        association = AccomplishmentTitleORM(accomplishment_id=title_orm.id, mission_id=accomplishment_orm.id)
        session.add(association)
        session.commit()
        domain.accomplishments.append(accomplishment)
        accomplishment.titles.append(domain)
        return domain
    elif control == "unlink":
        title_orm=title_domain_to_orm(domain)
        accomplishment_orm=accomplishment_domain_to_orm(accomplishment)
        association=session.query(AccomplishmentTitleORM).filter(and_(
            AccomplishmentTitleORM.title_id == title_orm.id,
            AccomplishmentTitleORM.accomplishment_id == accomplishment_orm.id
        )).first()
        
        session.delete(association)
        session.commit()
        domain.accomplishments= [acc for acc in domain.accomplishments  if acc.name != accomplishment.name]
        accomplishment.titles= [t for t in accomplishment.titles if t.name != domain.name]
        return domain
    else:
        print("invalid control")


def delete_title(domain:Title):
    from src.models.db.models import StatusTitleORM, AccomplishmentTitleORM
    orm = title_domain_to_orm(domain)
    target_id = orm.id
    session.query(StatusTitleORM).filter(StatusTitleORM.title_id == target_id).delete(synchronize_session=False)
    session.query(AccomplishmentTitleORM).filter(AccomplishmentTitleORM.title_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain
    