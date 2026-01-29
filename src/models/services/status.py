# perform a compound activity
from src.models.db.models import AttributeORM, StatusORM
from src.models.domain.status import Attribute, Status
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.db.models import BaseActivityAttributeORM
    
# view attributes
# update attributes
# delete attribute

# what services do i need for status

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

def populate_base_activities(domain:Attribute, associations:list["BaseActivityAttributeORM"]):
    from src.models.services.activity import activity_orm_to_domain
    for link in associations:
        temp_domain=activity_orm_to_domain(link.base_activity)
        temp_domain.load=link.load
        domain.base_activities.append(temp_domain)
    return domain

#_____________________________________________________#

def view_attributes(search:str | None=None) -> list[Attribute]: 
    if not search:
        professions = session.query(AttributeORM).all()
        domain_missions = [attribute_orm_to_domain(orm) for orm in professions] 
        return domain_missions
    else:
        professions = session.query(AttributeORM).filter(AttributeORM.name.ilike(f"%{search}%")).all()
        domain_professions = [attribute_orm_to_domain(orm) for orm in professions] 
        return domain_professions

def update_attribute(
        domain:Attribute,
        new_name: str | None = None, 
        new_area:str | None = None,
        new_custom: bool | None = None,
        new_current_value: float | None = None,
        ) ->Attribute:
    orm:AttributeORM  = attribute_domain_to_orm(domain)
    if not orm:
        orm: AttributeORM = create_attribute_orm(domain)
        session.add(orm)
        
    orm.name = new_name if new_name is not None else orm.name 
    domain.name = new_name if new_name is not None else domain.name
    
    orm.area = new_area if new_area is not None else orm.area 
    domain.area = new_area if new_area is not None else domain.area
    
    orm.custom = new_custom if new_custom is not None else orm.custom 
    domain.custom = new_custom if new_custom is not None else domain.custom
    
    orm.current_value = new_current_value if new_current_value is not None else orm.current_value 
    domain.current_value = new_current_value if new_current_value is not None else domain.current_value
    
    session.commit()
    
    return domain

def delete_attribute(domain:Attribute):
    from src.models.db.models import StatusAttributeORM, BaseActivityAttributeORM, AccomplishmentAttributeORM
    orm = attribute_domain_to_orm(domain)
    target_id = orm.id
    session.query(StatusAttributeORM).filter(StatusAttributeORM.attribute_id == target_id).delete(synchronize_session=False)
    session.query(BaseActivityAttributeORM).filter(BaseActivityAttributeORM.attribute_id == target_id).delete(synchronize_session=False)
    session.query(AccomplishmentAttributeORM).filter(AccomplishmentAttributeORM.attribute_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain

#______________________________________________________# status services
# create, persist, edit, link, reset, status

def status_orm_to_domain(orm: StatusORM)->Status:
    domain:Status = Status(xp=orm.xp, level=orm.level)
    domain.id=orm.id
    return domain

def status_domain_to_orm(domain: Status) -> StatusORM:
    status:Any = session.query(AttributeORM).first()
    return status

def create_status_orm(domain: Status) -> StatusORM:
    orm = StatusORM(xp=domain.xp, level=domain.level)
    return orm

def persist_status_orm(orm:StatusORM):
    existing = session.query(StatusORM)
    if existing.all()==[]:
        session.add(orm)
        session.commit()
    else:
        pass
        # how to handle this
        # old_orm=existing.first()
        # old_orm.xp = orm.xp
        # old_orm.level = orm.level

def update_mission(
        domain:Status,
        new_xp: float | None = None, 
        new_level:int | None = None,
        ) ->Status:
    orm:StatusORM  = status_domain_to_orm(domain)
    if not orm:
        orm: StatusORM = create_status_orm(domain)
        session.add(orm)
        
    orm.xp = new_xp if new_xp is not None else orm.xp 
    domain.xp = new_xp if new_xp is not None else domain.xp
    
    orm.level = new_level if new_level is not None else orm.level 
    domain.level = new_level if new_level is not None else domain.level
    
    session.commit()
    
    return domain

