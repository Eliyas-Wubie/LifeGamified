from src.models.db.models import MissionORM
from src.models.domain.mission import Mission
from typing import Any, TYPE_CHECKING
from datetime import datetime
from src.models.db.session import SessionLocal
from sqlalchemy import or_, and_

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.accomplishment import Accomplishment
    from src.models.domain.profession import Profession

# view and search mission
# create mission
# edit mission
# delete mission
# link mission
 
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

def view_missions(search:str | None=None) -> list[Mission]: 
    if not search:
        missions = session.query(MissionORM).all()
        domain_missions = [mission_orm_to_domain(orm) for orm in missions] 
        return domain_missions
    else:
        missions = session.query(MissionORM).filter(or_(
            MissionORM.name.ilike(f"%{search}%"),
            MissionORM.description.ilike(f"%{search}%"),                     
        )).all()
        domain_missions = [mission_orm_to_domain(orm) for orm in missions] 
        return domain_missions

def update_mission(
        domain:Mission,
        new_name: str | None = None, 
        new_description:str | None = None,
        new_deadline: datetime | None = None,
        new_bonus: list[dict[str,Any]] | None = None,
        ) ->Mission:
    orm:MissionORM  = mission_domain_to_orm(domain)
    if not orm:
        orm: MissionORM = create_mission_orm(domain)
        session.add(orm)
    orm.name = new_name if new_name is not None else orm.name 
    domain.name = new_name if new_name is not None else domain.name
    
    orm.description = new_description if new_description is not None else orm.description 
    domain.description = new_description if new_description is not None else domain.description
    
    orm.deadline = new_deadline if new_deadline is not None else orm.deadline 
    domain.deadline = new_deadline if new_deadline is not None else domain.deadline
    
    orm.bonus = new_bonus if new_bonus is not None else orm.bonus 
    domain.bonus = new_bonus if new_bonus is not None else domain.bonus
    
    session.commit()
    
    return domain

def control_mission_compound_activity_link(control:str, domain:Mission,compound_activity: "CompoundActivity", load:int | None = None):
    from src.models.db.models import CompoundActivityMissionORM
    from src.models.services.activity import compound_activity_domain_to_orm
    
    load = 1 if load is None else load
    if control == "link":
        mission_orm=mission_domain_to_orm(domain)
        compound_activity_orm=compound_activity_domain_to_orm(compound_activity)
        association = CompoundActivityMissionORM(mission_id=mission_orm.id, compound_activity_id=compound_activity_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.compound_activities.append(compound_activity)
        compound_activity.missions.append(domain)
        return domain
    elif control == "unlink":
        mission_orm=mission_domain_to_orm(domain)
        compound_activity_orm=compound_activity_domain_to_orm(compound_activity)
        association=session.query(CompoundActivityMissionORM).filter(and_(
            CompoundActivityMissionORM.mission_id == mission_orm.id,
            CompoundActivityMissionORM.compound_activity_id == compound_activity_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.compound_activities= [act for act in domain.compound_activities if act.name != compound_activity.name]
        compound_activity.missions= [mission for mission in compound_activity.missions  if mission.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_mission_accomplishment_link(control:str, domain:Mission,accomplishment: "Accomplishment", load:int | None = None):
    from src.models.db.models import MissionAccomplishmentORM
    from src.models.services.accomplishment import create_accomplishment_orm
    load = 1 if load is None else load
    if control == "link":
        mission_orm=mission_domain_to_orm(domain)
        accomplishment_orm=create_accomplishment_orm(accomplishment)
        association = MissionAccomplishmentORM(mission_id=mission_orm.id, accomplishment_id=accomplishment_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.accomplishments.append(accomplishment)
        accomplishment.missions.append(domain)
        return domain
    elif control == "unlink":
        mission_orm=mission_domain_to_orm(domain)
        accomplishment_orm=create_accomplishment_orm(accomplishment)
        association=session.query(MissionAccomplishmentORM).filter(and_(
            MissionAccomplishmentORM.mission_id == mission_orm.id,
            MissionAccomplishmentORM.accomplishment_id == accomplishment_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.accomplishments= [acc for acc in domain.accomplishments  if acc.name != accomplishment.name]
        accomplishment.missions= [mission for mission in accomplishment.missions  if mission.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_mission_profession_link(control:str, domain:Mission,profession: "Profession", load:int | None = None):
    from src.models.db.models import MissionProfessionORM
    from src.models.services.profession import profession_domain_to_orm
    load = 1 if load is None else load
    if control == "link":
        mission_orm=mission_domain_to_orm(domain)
        profession_orm=profession_domain_to_orm(profession)
        association = MissionProfessionORM(mission_id=mission_orm.id, profession_id=profession_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.professions.append(profession)
        profession.missions.append(domain)
        return domain
    elif control == "unlink":
        mission_orm=mission_domain_to_orm(domain)
        profession_orm=profession_domain_to_orm(profession)
        association=session.query(MissionProfessionORM).filter(and_(
            MissionProfessionORM.mission_id == mission_orm.id,
            MissionProfessionORM.profession_id == profession_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.professions= [prof for prof in domain.professions  if prof.name != profession.name]
        profession.missions= [c_act for c_act in profession.missions  if c_act.name != domain.name]
        return domain
    else:
        print("invalid control")

def delete_mission(domain:Mission):
    from src.models.db.models import CompoundActivityMissionORM, MissionAccomplishmentORM, MissionProfessionORM
    orm = mission_domain_to_orm(domain)
    target_id = orm.id
    session.query(CompoundActivityMissionORM).filter(CompoundActivityMissionORM.mission_id == target_id).delete(synchronize_session=False)
    session.query(MissionAccomplishmentORM).filter(MissionAccomplishmentORM.mission_id == target_id).delete(synchronize_session=False)
    session.query(MissionProfessionORM).filter(MissionProfessionORM.mission_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain

