from typing import TYPE_CHECKING, Any

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.models.db.models import AccomplishmentORM
from src.models.db.session import SessionLocal
from src.models.domain.accomplishment import Accomplishment

if TYPE_CHECKING:
    from src.models.domain.mission import Mission
    from src.models.domain.profession import Profession
    from src.models.domain.status import Attribute
    from src.models.domain.titles import Title


def accomplishment_orm_to_domain(orm: AccomplishmentORM) -> Accomplishment:
    from src.models.services.mission import mission_orm_to_domain
    from src.models.services.profession import profession_orm_to_domain
    from src.models.services.status import attribute_orm_to_domain
    from src.models.services.title import title_orm_to_domain

    attributes: list["Attribute"] = []
    professions: list["Profession"] = []
    titles: list["Title"] = []
    missions: list["Mission"] = []
    for association in orm.attributes:
        temp_domain = attribute_orm_to_domain(association.attribute)
        temp_domain.load = association.load
        attributes.append(temp_domain)
    for association in orm.professions:
        temp_domain = profession_orm_to_domain(association.profession)
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


def accomplishment_domain_to_orm(
    domain: Accomplishment, session: Session
) -> AccomplishmentORM:
    accomplishment: Any = (
        session.query(AccomplishmentORM)
        .filter(AccomplishmentORM.name == domain.name)
        .first()
    )
    return accomplishment


def create_accomplishment_orm(domain: Accomplishment) -> AccomplishmentORM:
    return AccomplishmentORM(
        name=domain.name, description=domain.description, difficulty=domain.difficulty
    )


def view_owned_accomplishments(search: str | None = None) -> list[Accomplishment]:
    with SessionLocal() as session:
        if not search:
            accomplishments: Any = (
                session.query(AccomplishmentORM)
                .filter(AccomplishmentORM.status == "unlocked")
                .all()
            )
            return [accomplishment_orm_to_domain(orm) for orm in accomplishments]

        accomplishments = (
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
        return [accomplishment_orm_to_domain(orm) for orm in accomplishments]


def view_unowned_accomplishments(search: str | None = None) -> list[Accomplishment]:
    with SessionLocal() as session:
        if not search:
            accomplishments: Any = (
                session.query(AccomplishmentORM)
                .filter(AccomplishmentORM.status == "locked")
                .all()
            )
            return [accomplishment_orm_to_domain(orm) for orm in accomplishments]

        accomplishments = (
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
        return [accomplishment_orm_to_domain(orm) for orm in accomplishments]


def view_accomplishments(search: str | None = None) -> list[Accomplishment]:
    with SessionLocal() as session:
        if not search:
            accomplishments: Any = session.query(AccomplishmentORM).all()
            return [accomplishment_orm_to_domain(orm) for orm in accomplishments]

        accomplishments = (
            session.query(AccomplishmentORM)
            .filter(
                or_(
                    AccomplishmentORM.name.ilike(f"%{search}%"),
                    AccomplishmentORM.description.ilike(f"%{search}%"),
                )
            )
            .all()
        )
        return [accomplishment_orm_to_domain(orm) for orm in accomplishments]


def create_accomplishment(orm: AccomplishmentORM):
    with SessionLocal() as session:
        session.add(orm)
        session.commit()


def update_accomplishment(
    domain: Accomplishment,
    new_name: str | None = None,
    new_description: str | None = None,
    new_difficulty: int | None = None,
    new_status: str | None = None,
) -> Accomplishment:
    with SessionLocal() as session:
        orm: AccomplishmentORM = accomplishment_domain_to_orm(domain, session)
        if not orm:
            orm = create_accomplishment_orm(domain)

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
    from src.models.db.models import AccomplishmentAttributeORM
    from src.models.services.status import attribute_domain_to_orm

    load = 1 if load is None else load
    with SessionLocal() as session:
        if control == "link":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            attribute_orm = attribute_domain_to_orm(attribute, session)
            association = AccomplishmentAttributeORM(
                accomplishment_id=accomplishment_orm.id,
                attribute_id=attribute_orm.id,
                load=load,
            )
            session.add(association)
            session.commit()
            domain.attributes.append(attribute)
            return domain
        if control == "unlink":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            attribute_orm = attribute_domain_to_orm(attribute, session)
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


def control_accomplishment_profession_link(
    control: str,
    domain: Accomplishment,
    profession: "Profession",
    load: int | None = None,
):
    from src.models.db.models import AccomplishmentProfessionORM
    from src.models.services.profession import profession_domain_to_orm

    load = 1 if load is None else load
    with SessionLocal() as session:
        if control == "link":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            profession_orm = profession_domain_to_orm(profession, session)
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
        if control == "unlink":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            profession_orm = profession_domain_to_orm(profession, session)
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


def control_accomplishment_mission_link(
    control: str, domain: Accomplishment, mission: "Mission"
):
    from src.models.db.models import MissionAccomplishmentORM
    from src.models.services.mission import mission_domain_to_orm

    with SessionLocal() as session:
        if control == "link":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            mission_orm = mission_domain_to_orm(mission, session)
            association = MissionAccomplishmentORM(
                accomplishment_id=accomplishment_orm.id, mission_id=mission_orm.id
            )
            session.add(association)
            session.commit()
            domain.missions.append(mission)
            mission.accomplishments.append(domain)
            return domain
        if control == "unlink":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            mission_orm = mission_domain_to_orm(mission, session)
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


def control_accomplishment_title_link(
    control: str, domain: Accomplishment, title: "Title"
):
    from src.models.db.models import AccomplishmentTitleORM
    from src.models.services.title import title_domain_to_orm

    with SessionLocal() as session:
        if control == "link":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            title_orm = title_domain_to_orm(title, session)
            association = AccomplishmentTitleORM(
                accomplishment_id=accomplishment_orm.id, title_id=title_orm.id
            )
            session.add(association)
            session.commit()
            domain.titles.append(title)
            title.accomplishments.append(domain)
            return domain
        if control == "unlink":
            accomplishment_orm = accomplishment_domain_to_orm(domain, session)
            title_orm = title_domain_to_orm(title, session)
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


def delete_accomplishment(domain: Accomplishment):
    from src.models.db.models import (
        AccomplishmentAttributeORM,
        AccomplishmentProfessionORM,
        AccomplishmentTitleORM,
        MissionAccomplishmentORM,
    )

    with SessionLocal() as session:
        orm = accomplishment_domain_to_orm(domain, session)
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
