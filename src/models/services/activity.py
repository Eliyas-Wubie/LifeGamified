# create compound activity
# create a base actvity - sync/other
# perform a compound activity
from src.models.db.models import BaseActivityORM
from src.models.domain.activity import Activity
from src.models.services.status import attribute_orm_to_domain
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def activity_orm_to_domain(orm: BaseActivityORM | None, base_activity_class: type[Activity])->Any:
    strain:Any = []
    if orm is None:
        return None
    for association in orm.strain:
        temp_domain=attribute_orm_to_domain(association.attributes)
        temp_domain.load=association.rating
        strain.append(temp_domain)
    domain:Activity = base_activity_class(orm.name, orm.baseXP, strain)
    domain.id=orm.id
    return domain

def activity_domain_to_orm(domain: Activity) -> BaseActivityORM:
    activity:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
    print(activity)
    return activity

def activity_create_orm_from_domain(domain: Activity) -> BaseActivityORM:
    orm = BaseActivityORM(name=domain.name, baseXP=domain.baseXP)
    return orm