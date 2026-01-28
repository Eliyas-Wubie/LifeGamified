from src.models.domain.profession import Profession
from src.models.db.models import ProfessionORM
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.mission import Mission
    from src.models.domain.accomplishment import Accomplishment
    
# view profession tree
# register profession tree
# edit profession tree
# delete profession tree
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
