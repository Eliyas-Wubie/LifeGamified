from src.models.domain.profession import Profession
from src.models.db.models import ProfessionORM
from src.models.services.activity import compound_activity_orm_to_domain
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def profession_orm_to_domain(orm: ProfessionORM) -> Profession:
    domain = Profession(orm.label, orm.status)
    for sub in orm.sub_professions:
        domain.add_sub_profession(profession_orm_to_domain(sub))
    domain.parent=None if orm.parent is None else profession_orm_to_domain(orm.parent)
    domain.compound_activity_links=[compound_activity_orm_to_domain(c_act.compound_activity) for c_act in orm.compound_activity_links]
    # handle mission links
    # handle accomplishment links
    return domain

def profession_domain_to_orm(domain: Profession) -> ProfessionORM:
    prof:Any = session.query(ProfessionORM).filter(ProfessionORM.label == domain.label).first()
    return prof
def profession_create_orm_from_domain(
    domain: Profession,
    cache: dict[int, ProfessionORM] | None = None,
) -> ProfessionORM:
    if cache is None:
        cache = {}

    key = id(domain)
    if key in cache:
        return cache[key]

    orm = ProfessionORM(
        label=domain.label,
        status=domain.status,
    )
    cache[key] = orm

    orm.sub_professions = [
        profession_create_orm_from_domain(child, cache)
        for child in domain.sub_professions
    ]

    return orm
