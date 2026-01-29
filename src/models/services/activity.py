from src.models.db.models import BaseActivityORM, CompoundActivityORM
from src.models.domain.activity import BaseActivity, CompoundActivity
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal
from sqlalchemy import and_

if TYPE_CHECKING:
    from src.models.domain.status import Attribute
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.activity import BaseActivity
    from src.models.domain.profession import Profession
    from src.models.domain.mission import Mission
        
session = SessionLocal()

def activity_orm_to_domain(orm: BaseActivityORM )->BaseActivity:
    from src.models.services.status import attribute_orm_to_domain
    
    attributes:list["Attribute"] = []
    compound_activities:list["CompoundActivity"]= []
    for association in orm.attributes:
        temp_domain=attribute_orm_to_domain(association.attribute)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        attributes.append(temp_domain)
    for association in orm.compound_activities:
        temp_domain=compound_activity_orm_to_domain(association.compound_activity)    # handle by creating a new function in a different file?
        temp_domain.load=association.load
        compound_activities.append(temp_domain)
    domain:BaseActivity = BaseActivity(orm.name, orm.xp, attributes=attributes)
    domain.id=orm.id
    domain.activity_type=orm.activity_type
    domain.compound_activities=compound_activities
    return domain

def activity_domain_to_orm(domain: BaseActivity) -> BaseActivityORM:
    activity:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
    return activity

def create_activity_orm(domain: BaseActivity) -> BaseActivityORM:
    # enforce rule - can only create custom basic activities if type is other
    if domain.activity_type == "other":
        orm = BaseActivityORM(name=domain.name, xp=domain.xp, activity_type="other")
        return orm
    else:
        existing_orm=session.query(BaseActivityORM).filter(BaseActivityORM.name == domain.name).first()
        if existing_orm:
            return existing_orm
        else:
            # create relationships ?
            return BaseActivityORM(name=domain.name, xp=domain.xp, activity_type=domain.activity_type)



def view_basic_activities(search:str | None=None) -> list[BaseActivity]: 
    if not search:
        basic_activities:Any = session.query(BaseActivityORM).all()
        domain_basic_activities = [activity_orm_to_domain(orm) for orm in basic_activities] 
        return domain_basic_activities
    else:
        basic_activities:Any = session.query(BaseActivityORM).filter(BaseActivityORM.name.ilike(f"%{search}%")).all()
        domain_basic_activities = [activity_orm_to_domain(orm) for orm in basic_activities] 
        return domain_basic_activities

def update_basic_activity(
        domain:BaseActivity,
        new_name: str | None = None, 
        new_xp:float | None = None,
        new_activity_type: str | None = None,
        ) ->BaseActivity:
    orm:BaseActivityORM  = activity_domain_to_orm(domain)
    if not orm:
        orm: BaseActivityORM = create_activity_orm(domain)
        session.add(orm)
        
    orm.name = new_name if new_name is not None else orm.name # type: ignore
    domain.name = new_name if new_name is not None else domain.name
    
    orm.xp = new_xp if new_xp is not None else orm.xp # type: ignore
    domain.xp = new_xp if new_xp is not None else domain.xp
    
    orm.activity_type = new_activity_type if new_activity_type is not None else orm.activity_type # type: ignore
    domain.activity_type = new_activity_type if new_activity_type is not None else domain.activity_type
    
    session.commit()
    
    return domain

def control_basic_activity_attribute_link(control:str, domain:BaseActivity,attribute: "Attribute", load:int | None = None):
    from src.models.services.status import attribute_domain_to_orm
    from src.models.db.models import BaseActivityAttributeORM
    load = 1 if load is None else load
    if control == "link":
        accomplishment_orm=activity_domain_to_orm(domain)
        attribute_orm=attribute_domain_to_orm(attribute)
        association = BaseActivityAttributeORM(accomplishment_id=accomplishment_orm.id, attribute_id=attribute_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.attributes.append(attribute)
        attribute.base_activities.append(domain)
        return domain
    elif control == "unlink":
        accomplishment_orm=activity_domain_to_orm(domain)
        attribute_orm=attribute_domain_to_orm(attribute)
        association=session.query(BaseActivityAttributeORM).filter(and_(
            BaseActivityAttributeORM.base_activity_id == accomplishment_orm.id,
            BaseActivityAttributeORM.attribute_id == attribute_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.attributes= [attr for attr in domain.attributes  if attr.name != attribute.name]
        attribute.base_activities= [act for act in attribute.base_activities  if act.name != domain.name]
        return domain
    else:
        print("invalid control")

def delete_basic_activity(domain:BaseActivity):
    from src.models.db.models import BaseActivityAttributeORM, BaseActivityCompoundActivityORM
    orm = activity_domain_to_orm(domain)
    target_id = orm.id
    session.query(BaseActivityAttributeORM).filter(BaseActivityAttributeORM.base_activity_id == target_id).delete(synchronize_session=False)
    session.query(BaseActivityCompoundActivityORM).filter(BaseActivityCompoundActivityORM.base_activity_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain


def compound_activity_orm_to_domain(orm: CompoundActivityORM )->CompoundActivity:
    from src.models.services.profession import profession_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain
    
    activities:list["BaseActivity"] = []
    professions:list["Profession"]=[]
    missions:list["Mission"]=[]

    for association in orm.base_activities:
        temp_domain=activity_orm_to_domain(association.base_activity) 
        temp_domain.load=association.load
        activities.append(temp_domain)
    for association in orm.professions:
        temp_domain=profession_orm_to_domain(association.profession)
        temp_domain.load=association.load
        professions.append(temp_domain)
    for association in orm.missions:
        temp_domain=mission_orm_to_domain(association.mission)
        missions.append(temp_domain)

    domain:CompoundActivity = CompoundActivity(orm.name, orm.xp, orm.tags, activities, professions, missions)
    domain.id=orm.id
    return domain

def compound_activity_domain_to_orm(domain: CompoundActivity) -> CompoundActivityORM:
    c_activity:Any = session.query(CompoundActivityORM).filter(CompoundActivityORM.name == domain.name).first()
    return c_activity

def create_compound_activity_orm(domain: CompoundActivity) -> CompoundActivityORM:
    orm = CompoundActivityORM(name=domain.name, xp=domain.xp)
    return orm

def view_compound_activities(search:str | None=None, tag:str | None = None) -> list[CompoundActivity]: 
    if not search:
        if tag is None:
            compound_activities:Any = session.query(CompoundActivityORM).all()
        else:
            compound_activities_unfiltered = session.query(CompoundActivityORM)
            compound_activities = compound_activities_unfiltered.filter(CompoundActivityORM.tags.contains([tag]))
        domain_compound_activities = [compound_activity_orm_to_domain(orm) for orm in compound_activities] 
        return domain_compound_activities
    else:
        if tag is None:
            compound_activities:Any = session.query(CompoundActivityORM).filter(CompoundActivityORM.name.ilike(f"%{search}%")).all()
        else:
            compound_activities_unfiltered = session.query(CompoundActivityORM)
            compound_activities = compound_activities_unfiltered.filter(CompoundActivityORM.tags.contains([tag])).filter(CompoundActivityORM.name.ilike(f"%{search}%")).all()
        domain_compound_activities = [compound_activity_orm_to_domain(orm) for orm in compound_activities] 
        return domain_compound_activities

def update_compound_activity(
        domain:CompoundActivity,
        new_name: str | None = None, 
        new_xp:float | None = None,
        new_tags: list[str] | None = None,
        ) ->CompoundActivity:
    orm:CompoundActivityORM  = compound_activity_domain_to_orm(domain)
    if not orm:
        orm: CompoundActivityORM = create_compound_activity_orm(domain)
        session.add(orm)
    orm.name = new_name if new_name is not None else orm.name 
    domain.name = new_name if new_name is not None else domain.name
    
    orm.xp = new_xp if new_xp is not None else orm.xp 
    domain.xp = new_xp if new_xp is not None else domain.xp
    
    orm.tags = new_tags if new_tags is not None else orm.tags 
    domain.tags = new_tags if new_tags is not None else domain.tags
    
    session.commit()
    
    return domain

def control_compound_activity_activity_link(control:str, domain:CompoundActivity,base_activity: BaseActivity, load:int | None = None):

    from src.models.db.models import BaseActivityCompoundActivityORM
    load = 1 if load is None else load
    if control == "link":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        base_activity_orm=activity_domain_to_orm(base_activity)
        association = BaseActivityCompoundActivityORM(compound_activity_id=compound_activity_orm.id, base_activity_id=base_activity_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.activities.append(base_activity)
        base_activity.compound_activities.append(domain)
        return domain
    elif control == "unlink":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        base_activity_orm=activity_domain_to_orm(base_activity)
        association=session.query(BaseActivityCompoundActivityORM).filter(and_(
            BaseActivityCompoundActivityORM.compound_activity_id == compound_activity_orm.id,
            BaseActivityCompoundActivityORM.base_activity_id == base_activity_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.activities= [act for act in domain.activities  if act.name != base_activity.name]
        base_activity.compound_activities= [c_act for c_act in base_activity.compound_activities  if c_act.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_compound_activity_profession_link(control:str, domain:CompoundActivity,profession: "Profession", load:int | None = None):
    from src.models.db.models import CompoundActivityProfessionORM
    from src.models.services.profession import profession_domain_to_orm
    
    load = 1 if load is None else load
    if control == "link":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        base_activity_orm=profession_domain_to_orm(profession)
        association = CompoundActivityProfessionORM(compound_activity_id=compound_activity_orm.id, profession_id=base_activity_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.professions.append(profession)
        profession.compound_activities.append(domain)
        return domain
    elif control == "unlink":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        base_activity_orm=profession_domain_to_orm(profession)
        association=session.query(CompoundActivityProfessionORM).filter(and_(
            CompoundActivityProfessionORM.compound_activity_id == compound_activity_orm.id,
            CompoundActivityProfessionORM.profession_id == base_activity_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.professions= [prof for prof in domain.professions if prof.name != profession.name]
        profession.compound_activities= [c_act for c_act in profession.compound_activities  if c_act.name != domain.name]
        return domain
    else:
        print("invalid control")

def control_compound_activity_mission_link(control:str, domain:CompoundActivity,mission: "Mission", load:int | None = None):
    from src.models.db.models import CompoundActivityMissionORM
    from src.models.services.mission import mission_domain_to_orm
    
    load = 1 if load is None else load
    if control == "link":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        mission_orm=mission_domain_to_orm(mission)
        association = CompoundActivityMissionORM(compound_activity_id=compound_activity_orm.id, mission_id=mission_orm.id, load=load)
        session.add(association)
        session.commit()
        domain.missions.append(mission)
        mission.compound_activities.append(domain)
        return domain
    elif control == "unlink":
        compound_activity_orm=compound_activity_domain_to_orm(domain)
        mission_orm=mission_domain_to_orm(mission)
        association=session.query(CompoundActivityMissionORM).filter(and_(
            CompoundActivityMissionORM.compound_activity_id == compound_activity_orm.id,
            CompoundActivityMissionORM.mission_id == mission_orm.id
        )).first()
        session.delete(association)
        session.commit()
        domain.missions= [mission for mission in domain.missions  if mission.name != mission.name]
        mission.compound_activities= [c_act for c_act in mission.compound_activities  if c_act.name != domain.name]
        return domain
    else:
        print("invalid control")

def delete_compound_activity(domain:CompoundActivity):
    from src.models.db.models import CompoundActivityMissionORM, CompoundActivityProfessionORM, BaseActivityCompoundActivityORM
    orm = compound_activity_domain_to_orm(domain)
    target_id = orm.id
    session.query(CompoundActivityMissionORM).filter(CompoundActivityMissionORM.compound_activity_id == target_id).delete(synchronize_session=False)
    session.query(CompoundActivityProfessionORM).filter(CompoundActivityProfessionORM.compound_activity_id == target_id).delete(synchronize_session=False)
    session.query(BaseActivityCompoundActivityORM).filter(BaseActivityCompoundActivityORM.compound_activity_id == target_id).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain

