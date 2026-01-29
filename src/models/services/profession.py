from src.models.domain.profession import Profession
from src.models.db.models import ProfessionORM
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal
from sqlalchemy.orm import joinedload
from sqlalchemy import and_

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.mission import Mission
    from src.models.domain.accomplishment import Accomplishment
    
# view profession tree
# create profession
# edit profession
# delete profession
# link profession
# update profession    

session = SessionLocal()

def profession_orm_to_domain(orm: ProfessionORM) -> Profession:
    # can we check cache here too
    from src.models.services.activity import compound_activity_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain
    from src.models.services.accomplishment import accomplishment_orm_to_domain
    
    compound_activities: list["CompoundActivity"]=[]
    missions: list["Mission"]=[]
    accomplishments: list["Accomplishment"]=[]
    
    for association in orm.compound_activities:
        temp_domain=compound_activity_orm_to_domain(association.compound_activity)
        temp_domain.load=association.load
        compound_activities.append(temp_domain)
    
    for association in orm.missions:
        temp_domain=mission_orm_to_domain(association.mission)
        temp_domain.load=association.load
        missions.append(temp_domain)
        
    for association in orm.accomplishments:
        temp_domain=accomplishment_orm_to_domain(association.accomplishment)
        temp_domain.load=association.load
        accomplishments.append(temp_domain)
     
    domain = Profession(orm.name, orm.status, orm.points)
    for sub in orm.sub_professions:
        domain.add_sub_profession(profession_orm_to_domain(sub))
    domain.parent=None if orm.parent is None else profession_orm_to_domain(orm.parent)
    domain.id=orm.id
    domain.compound_activities=compound_activities
    domain.missions=missions
    domain.accomplishments=accomplishments

    return domain

def profession_domain_to_orm(domain: Profession) -> ProfessionORM:
    # check cache
    prof:Any = session.query(ProfessionORM).filter(ProfessionORM.name == domain.name).first()
    return prof

def create_profession_orm(
    domain: Profession,
    cache: dict[int, ProfessionORM] | None = None,
) -> ProfessionORM:
    if cache is None:
        cache = {}

    key = id(domain)
    if key in cache:
        return cache[key]

    orm = ProfessionORM(
        name=domain.name,
        status=domain.status,
        points=domain.points
    )
    cache[key] = orm

    orm.sub_professions = [
        create_profession_orm(child, cache)
        for child in domain.sub_professions
    ]

    return orm

#_____________________________________________________________#

def view_professions(search:str | None=None) -> list[Profession]: 
    if not search:
        professions = session.query(ProfessionORM).all()
        domain_missions = [profession_orm_to_domain(orm) for orm in professions] 
        return domain_missions
    else:
        professions = session.query(ProfessionORM).filter(ProfessionORM.name.ilike(f"%{search}%")).all()
        domain_professions = [profession_orm_to_domain(orm) for orm in professions] 
        return domain_professions

def view_profession_tree():
    professions = session.query(ProfessionORM).filter(ProfessionORM.parent == None).options(joinedload(ProfessionORM.sub_professions)).all()
    return professions # if sub_profession with in sub_professions are not loaded then recursive logic may be needed here

def update_profession(
        domain:Profession,
        new_name: str | None = None, 
        new_status:str | None = None,
        new_points: float | None = None,
        new_parent: ProfessionORM | None = None,
        ) ->Profession:
    orm:ProfessionORM  = profession_domain_to_orm(domain)
    if not orm:
        orm: ProfessionORM = create_profession_orm(domain)
        session.add(orm)
        
    orm.name = new_name if new_name is not None else orm.name 
    domain.name = new_name if new_name is not None else domain.name
    
    orm.status = new_status if new_status is not None else orm.status 
    domain.status = new_status if new_status is not None else domain.status
    
    orm.points = new_points if new_points is not None else orm.points 
    domain.points = new_points if new_points is not None else domain.points
    
    
    orm.parent_id = new_parent.id if new_parent is not None else orm.parent_id 
    domain.parent = profession_orm_to_domain(new_parent) if new_parent is not None else domain.parent
    # sub_professions is automatically handled using the parent foreign key 
    # and relation as reversing it creates a sub_profession. these it is already handled
    
    session.commit()
    
    return domain

def control_profession_compound_activity_link(control:str, domain:Profession,compound_activity: "CompoundActivity", load:int | None = None):
    from src.models.db.models import CompoundActivityProfessionORM
    from src.models.services.activity import compound_activity_domain_to_orm
    
    load = 1 if load is None else load
    
    if control == "link":
        profession_orm=profession_domain_to_orm(domain)
        compound_activity_orm=compound_activity_domain_to_orm(compound_activity)
        association = CompoundActivityProfessionORM(profession_id=profession_orm.id, compound_activity_id=compound_activity_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.compound_activities.append(compound_activity)
        compound_activity.professions.append(domain)
        return domain
    elif control == "unlink":
        profession_orm=profession_domain_to_orm(domain)
        compound_activity_orm=compound_activity_domain_to_orm(compound_activity)
        association=session.query(CompoundActivityProfessionORM).filter(and_(
            CompoundActivityProfessionORM.profession_id == profession_orm.id,
            CompoundActivityProfessionORM.compound_activity_id == compound_activity_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.compound_activities= [act for act in domain.compound_activities if act.name != compound_activity.name]
        compound_activity.professions= [prof for prof in compound_activity.professions  if prof.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_profession_accomplishment_link(control:str, domain:Profession,accomplishment: "Accomplishment", load:int | None = None):
    from src.models.db.models import AccomplishmentProfessionORM
    from src.models.services.accomplishment import create_accomplishment_orm
    load = 1 if load is None else load
    if control == "link":
        profession_orm=profession_domain_to_orm(domain)
        accomplishment_orm=create_accomplishment_orm(accomplishment)
        association = AccomplishmentProfessionORM(profession_id=profession_orm.id, accomplishment_id=accomplishment_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.accomplishments.append(accomplishment)
        accomplishment.professions.append(domain)
        return domain
    elif control == "unlink":
        profession_orm=profession_domain_to_orm(domain)
        accomplishment_orm=create_accomplishment_orm(accomplishment)
        association=session.query(AccomplishmentProfessionORM).filter(and_(
            AccomplishmentProfessionORM.profession_id == profession_orm.id,
            AccomplishmentProfessionORM.accomplishment_id == accomplishment_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.accomplishments= [acc for acc in domain.accomplishments  if acc.name != accomplishment.name]
        accomplishment.professions= [mission for mission in accomplishment.professions  if mission.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_profession_mission_link(control:str, domain:Profession,mission: "Mission", load:int | None = None):
    from src.models.services.mission import mission_domain_to_orm
    from src.models.db.models import MissionProfessionORM

    load = 1 if load is None else load
    if control == "link":
        profession_orm=profession_domain_to_orm(domain)
        mission_orm=mission_domain_to_orm(mission)
        association = MissionProfessionORM(profession_id=profession_orm.id, mission_id=mission_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.missions.append(mission)
        mission.professions.append(domain)
        return domain
    elif control == "unlink":
        profession_orm=profession_domain_to_orm(domain)
        mission_orm=mission_domain_to_orm(mission)
        association=session.query(MissionProfessionORM).filter(and_(
            MissionProfessionORM.profession_id == profession_orm.id,
            MissionProfessionORM.mission_id == mission_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.missions= [m for m in domain.missions  if m.name != mission.name]
        mission.professions= [prof for prof in mission.professions  if prof.name != domain.name]
        return domain
    else:
        print("invalid control")

def delete_profession(domain:Profession):
    from src.models.db.models import MissionProfessionORM, AccomplishmentProfessionORM, CompoundActivityProfessionORM
    orm = profession_domain_to_orm(domain)
    target_id = orm.id
    session.query(CompoundActivityProfessionORM).filter(CompoundActivityProfessionORM.profession_id == target_id).delete(synchronize_session=False)
    session.query(AccomplishmentProfessionORM).filter(AccomplishmentProfessionORM.profession_id == target_id).delete(synchronize_session=False)
    session.query(MissionProfessionORM).filter(MissionProfessionORM.profession_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain

