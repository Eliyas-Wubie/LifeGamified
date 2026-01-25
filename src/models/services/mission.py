from src.models.db.models import MissionsORM
from src.models.domain.mission import Mission
from typing import Any
from datetime import datetime
from src.models.db.session import SessionLocal

    
session = SessionLocal()

def mission_orm_to_domain(orm: MissionsORM | None)->Mission:
    from src.models.services.activity import compound_activity_orm_to_domain
    
    compound_activities:Any = []
    if orm is None:
        return None # type: ignore
    for c_act in orm.compound_activities:
        temp_domain=compound_activity_orm_to_domain(c_act.compound_activity)    # handle by creating a new function in a different file?
        temp_domain.load=c_act.rating
        compound_activities.append(temp_domain)
    domain:Mission = Mission(orm.name, compound_activities, datetime.now(), orm.bonus)
    domain.id=orm.id
    return domain

def mission_domain_to_orm(domain: Mission) -> MissionsORM:
    mission:Any = session.query(MissionsORM).filter(MissionsORM.name == domain.name).first()
    return mission

def mission_create_orm_from_domain(domain: Mission) -> MissionsORM:
    orm = MissionsORM(name=domain.name, deadline=domain.deadline, bonus=domain.bonus)
    return orm
