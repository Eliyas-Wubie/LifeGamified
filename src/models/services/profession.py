from src.models.domain.profession import Profession
from src.models.db.models import ProfessionORM
from typing import Any
from src.models.db.session import SessionLocal
    
session = SessionLocal()

def profession_orm_to_domain(orm: ProfessionORM) -> Profession:
    domain = Profession(orm.label, orm.status)
    for sub in orm.sub_professions:
        domain.add_sub_profession(profession_orm_to_domain(sub))
    return domain

def profession_domain_to_orm(domain: Profession) -> ProfessionORM:
    prof:Any = session.query(ProfessionORM).filter(ProfessionORM.label == domain.label).first()
    print(prof)
    return prof
def profession_create_orm_from_domain(domain: Profession) -> ProfessionORM:
    orm = ProfessionORM(label=domain.label, status=domain.status, sub_professions=[
        profession_create_orm_from_domain(prof) for prof in domain.sub_professions
        ])
    return orm