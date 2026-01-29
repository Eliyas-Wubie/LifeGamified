from src.models.db.models import AccomplishmentORM
from src.models.domain.accomplishment import Accomplishment
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal
from sqlalchemy import or_, and_

if TYPE_CHECKING:
    from src.models.domain.status import Attribute
    from src.models.domain.profession import Profession
    from src.models.domain.titles import Title
    from src.models.domain.mission import Mission

session = SessionLocal()


def accomplishment_orm_to_domain(orm: AccomplishmentORM) -> Accomplishment:
    from src.models.services.status import attribute_orm_to_domain
    from src.models.services.profession import profession_orm_to_domain
    from models.services.title import title_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain

    attributes: list["Attribute"] = []
    professions: list["Profession"] = []
    titles: list["Title"] = []
    missions: list["Mission"] = []
    for association in orm.attributes:
        temp_domain = attribute_orm_to_domain(
            association.attribute
        )  # handle by creating a new function in a different file?
        temp_domain.load = association.load
        attributes.append(temp_domain)
    for association in orm.professions:
        temp_domain = profession_orm_to_domain(
            association.profession
        )  # handle by creating a new function in a different file?
        temp_domain.load = association.load
        professions.append(temp_domain)
    for association in orm.titles:
        temp_domain = title_orm_to_domain(association.title)
        titles.append(temp_domain)
    for association in orm.missions:
        temp_domain = mission_orm_to_domain(association.mission)
        missions.append(temp_domain)

    domain: Accomplishment = Accomplishment(
        orm.name,
        orm.difficulty,
        orm.description,
        orm.status,
        attributes,
        professions,
        titles,
        missions,
    )
    domain.id = orm.id
    return domain


def accomplishment_domain_to_orm(domain: Accomplishment) -> AccomplishmentORM:
    Accomplishment: Any = (
        session.query(AccomplishmentORM)
        .filter(AccomplishmentORM.name == domain.name)
        .first()
    )
    return Accomplishment


def create_accomplishment_orm(domain: Accomplishment) -> AccomplishmentORM:
    orm = AccomplishmentORM(
        name=domain.name, description=domain.description, difficulty=domain.difficulty
    )
    return orm


def view_owned_accomplishments(search: str | None = None) -> list[Accomplishment]:
    if not search:
        accomplishments: Any = (
            session.query(AccomplishmentORM)
            .filter(AccomplishmentORM.status == "unlocked")
            .all()
        )
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments
    else:
        accomplishments: Any = (
            session.query(AccomplishmentORM)
            .filter(AccomplishmentORM.status == "unlocked")
            .filter(
                or_(
                    AccomplishmentORM.name.ilike(f"%{search}%"),
                    AccomplishmentORM.description.ilike(f"%{search}%"),
                )
            )
            .all()
        )
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments


def view_unowned_accomplishments(search: str | None = None) -> list[Accomplishment]:
    if not search:
        accomplishments: Any = (
            session.query(AccomplishmentORM)
            .filter(AccomplishmentORM.status == "locked")
            .all()
        )
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments
    else:
        accomplishments: Any = (
            session.query(AccomplishmentORM)
            .filter(AccomplishmentORM.status == "locked")
            .filter(
                or_(
                    AccomplishmentORM.name.ilike(f"%{search}%"),
                    AccomplishmentORM.description.ilike(f"%{search}%"),
                )
            )
            .all()
        )
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments


def view_accomplishments(search: str | None = None) -> list[Accomplishment]:
    if not search:
        accomplishments: Any = session.query(AccomplishmentORM).all()
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments
    else:
        accomplishments: Any = (
            session.query(AccomplishmentORM)
            .filter(
                or_(
                    AccomplishmentORM.name.ilike(f"%{search}%"),
                    AccomplishmentORM.description.ilike(f"%{search}%"),
                )
            )
            .all()
        )
        domain_accomplishments = [
            accomplishment_orm_to_domain(orm) for orm in accomplishments
        ]
        return domain_accomplishments


def create_accomplishment(orm: AccomplishmentORM):
    session.add(orm)
    session.commit()


def update_accomplishment(
    domain: Accomplishment,
    new_name: str | None = None,
    new_description: str | None = None,
    new_difficulty: int | None = None,
    new_status: str | None = None,
) -> Accomplishment:
    orm: AccomplishmentORM = accomplishment_domain_to_orm(domain)
    if not orm:
        orm: AccomplishmentORM = create_accomplishment_orm(domain)

    orm.name = new_name if new_name is not None else orm.name
    domain.name = new_name if new_name is not None else domain.name

    orm.difficulty = new_difficulty if new_difficulty is not None else orm.difficulty
    domain.difficulty = (
        new_difficulty if new_difficulty is not None else domain.difficulty
    )

    orm.description = (
        new_description if new_description is not None else orm.description
    )
    domain.description = (
        new_description if new_description is not None else domain.description
    )

    orm.status = new_status if new_status is not None else orm.status
    domain.status = new_status if new_status is not None else domain.status
    session.commit()

    return domain


def control_accomplishment_attribute_link(
    control: str,
    domain: Accomplishment,
    attribute: "Attribute",
    load: int | None = None,
):
    from src.models.services.status import attribute_domain_to_orm
    from src.models.db.models import AccomplishmentAttributeORM

    load = 1 if load is None else load
    if control == "link":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        attribute_orm = attribute_domain_to_orm(attribute)
        association = AccomplishmentAttributeORM(
            accomplishment_id=accomplishment_orm.id,
            attribute_id=attribute_orm.id,
            load=load,
        )
        session.add(association)
        session.commit()
        domain.attributes.append(attribute)
        return domain
    elif control == "unlink":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        attribute_orm = attribute_domain_to_orm(attribute)
        association = (
            session.query(AccomplishmentAttributeORM)
            .filter(
                and_(
                    AccomplishmentAttributeORM.accomplishment_id
                    == accomplishment_orm.id,
                    AccomplishmentAttributeORM.attribute_id == attribute_orm.id,
                )
            )
            .first()
        )
        session.delete(association)
        session.commit()
        domain.attributes = [
            attr for attr in domain.attributes if attr.name != attribute.name
        ]
        return domain
    else:
        print("invalid control")

    # get both the orms, get the id for both
    # remove the association


def control_accomplishment_profession_link(
    control: str,
    domain: Accomplishment,
    profession: "Profession",
    load: int | None = None,
):
    from src.models.services.profession import profession_domain_to_orm
    from src.models.db.models import AccomplishmentProfessionORM

    load = 1 if load is None else load
    if control == "link":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        profession_orm = profession_domain_to_orm(profession)
        association = AccomplishmentProfessionORM(
            accomplishment_id=accomplishment_orm.id,
            profession_id=profession_orm.id,
            load=load,
        )
        session.add(association)
        session.commit()
        domain.professions.append(profession)
        profession.accomplishments.append(domain)
        return domain
    elif control == "unlink":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        profession_orm = profession_domain_to_orm(profession)
        association = (
            session.query(AccomplishmentProfessionORM)
            .filter(
                and_(
                    AccomplishmentProfessionORM.accomplishment_id
                    == accomplishment_orm.id,
                    AccomplishmentProfessionORM.profession_id == profession_orm.id,
                )
            )
            .first()
        )

        session.delete(association)
        session.commit()
        domain.professions = [
            prof for prof in domain.professions if prof.name != profession.name
        ]
        profession.accomplishments = [
            acc for acc in profession.accomplishments if acc.name != domain.name
        ]
        return domain
    else:
        print("invalid control")


def control_accomplishment_mission_link(
    control: str, domain: Accomplishment, mission: "Mission"
):
    from src.models.services.mission import mission_domain_to_orm
    from src.models.db.models import MissionAccomplishmentORM

    if control == "link":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        mission_orm = mission_domain_to_orm(mission)
        association = MissionAccomplishmentORM(
            accomplishment_id=accomplishment_orm.id, mission_id=mission_orm.id
        )
        session.add(association)
        session.commit()
        domain.missions.append(mission)
        mission.accomplishments.append(domain)
        return domain
    elif control == "unlink":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        mission_orm = mission_domain_to_orm(mission)
        association = (
            session.query(MissionAccomplishmentORM)
            .filter(
                and_(
                    MissionAccomplishmentORM.accomplishment_id == accomplishment_orm.id,
                    MissionAccomplishmentORM.mission_id == mission_orm.id,
                )
            )
            .first()
        )

        session.delete(association)
        session.commit()
        domain.missions = [
            mission for mission in domain.missions if mission.name != mission.name
        ]
        mission.accomplishments = [
            acc for acc in mission.accomplishments if acc.name != domain.name
        ]
        return domain
    else:
        print("invalid control")


def control_accomplishment_title_link(
    control: str, domain: Accomplishment, title: "Title"
):
    from src.models.services.title import title_domain_to_orm
    from src.models.db.models import AccomplishmentTitleORM

    if control == "link":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        title_orm = title_domain_to_orm(title)
        association = AccomplishmentTitleORM(
            accomplishment_id=accomplishment_orm.id, title_id=title_orm.id
        )
        session.add(association)
        session.commit()
        domain.titles.append(title)
        title.accomplishments.append(domain)
        return domain
    elif control == "unlink":
        accomplishment_orm = accomplishment_domain_to_orm(domain)
        title_orm = title_domain_to_orm(title)
        association = (
            session.query(AccomplishmentTitleORM)
            .filter(
                and_(
                    AccomplishmentTitleORM.accomplishment_id == accomplishment_orm.id,
                    AccomplishmentTitleORM.title_id == title_orm.id,
                )
            )
            .first()
        )

        session.delete(association)
        session.commit()
        domain.titles = [t for t in domain.titles if t.name != title.name]
        title.accomplishments = [
            acc for acc in title.accomplishments if acc.name != domain.name
        ]
        return domain
    else:
        print("invalid control")


def delete_accomplishment(domain: Accomplishment):
    from src.models.db.models import (
        AccomplishmentAttributeORM,
        AccomplishmentProfessionORM,
        AccomplishmentTitleORM,
        MissionAccomplishmentORM,
    )

    orm = accomplishment_domain_to_orm(domain)
    target_id = orm.id
    session.query(AccomplishmentAttributeORM).filter(
        AccomplishmentAttributeORM.accomplishment_id == target_id
    ).delete(synchronize_session=False)
    session.query(AccomplishmentProfessionORM).filter(
        AccomplishmentProfessionORM.accomplishment_id == target_id
    ).delete(synchronize_session=False)
    session.query(AccomplishmentTitleORM).filter(
        AccomplishmentTitleORM.accomplishment_id == target_id
    ).delete(synchronize_session=False)
    session.query(MissionAccomplishmentORM).filter(
        MissionAccomplishmentORM.accomplishment_id == target_id
    ).delete(synchronize_session=False)
    session.delete(orm)
    session.commit()
    del domain
