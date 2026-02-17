# include a single activity in a daily report
# include a single mission in a daily report
# create a daily report
# save/persist daily report
from src.models.db.models import DailyReportORM
from src.models.domain.daily_report import DailyReport
from typing import Any, TYPE_CHECKING
from src.models.db.session import SessionLocal
from sqlalchemy import and_

if TYPE_CHECKING:
    from src.models.domain.activity import CompoundActivity
    from src.models.domain.mission import Mission

session = SessionLocal()


def daily_report_orm_to_domain(orm: DailyReportORM) -> DailyReport:
    from src.models.services.activity import compound_activity_orm_to_domain
    from src.models.services.mission import mission_orm_to_domain

    compound_activities: list["CompoundActivity"] = []
    missions: list["Mission"] = []
    for association in orm.compound_activities:
        temp_domain = compound_activity_orm_to_domain(
            association.compound_activity
        )  # handle by creating a new function in a different file?
        compound_activities.append(temp_domain)
    for association in orm.missions:
        temp_domain = mission_orm_to_domain(association.mission)
        missions.append(temp_domain)

    domain: DailyReport = DailyReport(orm.date, compound_activities, missions)
    domain.id = orm.id
    return domain


def daily_report_domain_to_orm(domain: DailyReport) -> DailyReportORM:
    DailyReport: Any = (
        session.query(DailyReportORM).filter(DailyReportORM.date == domain.date).first()
    )

    return DailyReport


def create_daily_report_orm(domain: DailyReport) -> DailyReportORM:
    orm = DailyReportORM(
        date=domain.date
    )
    return orm

def control_daily_report_compound_activity_link(
    control: str, domain: DailyReport, compound_activity: "CompoundActivity"
):
    from src.models.services.activity import compound_activity_domain_to_orm
    from src.models.db.models import DailyReportMissionORM

    if control == "link":
        daily_report_orm = daily_report_domain_to_orm(domain)
        compound_activity_orm = compound_activity_domain_to_orm(compound_activity)
        association = DailyReportMissionORM(
            daily_report_id=daily_report_orm.id, mission_id=compound_activity_orm.id
        )
        session.add(association)
        session.commit()
        domain.compound_activities.append(compound_activity)
        return domain
    elif control == "unlink":
        daily_report_orm = daily_report_domain_to_orm(domain)
        compound_activity_orm = compound_activity_domain_to_orm(compound_activity)
        association = (
            session.query(DailyReportMissionORM)
            .filter(
                and_(
                    DailyReportMissionORM.daily_report_id == daily_report_orm.id,
                    DailyReportMissionORM.mission_id == compound_activity_orm.id,
                )
            )
            .first()
        )

        session.delete(association)
        session.commit()
        domain.missions = [
            c_act for c_act in domain.missions if c_act.name != compound_activity.name
        ]
        return domain
    else:
        print("invalid control")

def control_daily_report_mission_link(
    control: str, domain: DailyReport, mission: "Mission"
):
    from src.models.services.mission import mission_domain_to_orm
    from src.models.db.models import DailyReportMissionORM

    if control == "link":
        daily_report_orm = daily_report_domain_to_orm(domain)
        mission_orm = mission_domain_to_orm(mission)
        association = DailyReportMissionORM(
            daily_report_id=daily_report_orm.id, mission_id=mission_orm.id
        )
        session.add(association)
        session.commit()
        domain.missions.append(mission)
        return domain
    elif control == "unlink":
        daily_report_orm = daily_report_domain_to_orm(domain)
        mission_orm = mission_domain_to_orm(mission)
        association = (
            session.query(DailyReportMissionORM)
            .filter(
                and_(
                    DailyReportMissionORM.daily_report_id == daily_report_orm.id,
                    DailyReportMissionORM.mission_id == mission_orm.id,
                )
            )
            .first()
        )

        session.delete(association)
        session.commit()
        domain.missions = [
            mission for mission in domain.missions if mission.name != mission.name
        ]
        return domain
    else:
        print("invalid control")

def report_daily_activity(daily_report: "DailyReport"): # persist
    session.add(daily_report)
    session.commit()
    

def get_all_reports()-> list[DailyReport]:
    orms = session.query(DailyReportORM).all()
    domains=[daily_report_orm_to_domain(orm) for orm in orms]
    return domains