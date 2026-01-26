from src.models.db.models import MissionORM
from src.models.domain.mission import Mission
from typing import Any, TYPE_CHECKING
from datetime import datetime
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.accomplishment import Accomplishment
    from src.models.domain.profession import Profession
    
session = SessionLocal()

def mission_orm_to_domain(orm: MissionORM )->Mission:
    from src.models.services.activity import compound_activity_orm_to_domain
    from src.models.services.accomplishment import accomplishment_orm_to_domain
    from src.models.services.profession import profession_orm_to_domain
    
    compound_activities:list["CompoundActivity"] = []
    accomplishments:list["Accomplishment"]=[]
    professions:list["Profession"]=[]

    for association in orm.compound_activities:
        temp_domain=compound_activity_orm_to_domain(association.compound_activity)    # handle by creating a new function in a different file?
        compound_activities.append(temp_domain)
    for association in orm.accomplishments:
        temp_domain=accomplishment_orm_to_domain(association.accomplishment)
        accomplishments.append(temp_domain)
    for association in orm.professions:
        temp_domain=profession_orm_to_domain(association.profession)
        temp_domain.load=association.load
        professions.append(temp_domain)
    domain:Mission = Mission(orm.name, orm.description, datetime.now(), orm.bonus, compound_activities,accomplishments,professions)
    domain.id=orm.id
    return domain

def mission_domain_to_orm(domain: Mission) -> MissionORM:
    mission:Any = session.query(MissionORM).filter(MissionORM.name == domain.name).first()
    return mission

def create_mission_orm(domain: Mission) -> MissionORM:
    orm = MissionORM(name=domain.name, deadline=domain.deadline, bonus=domain.bonus)
    return orm
