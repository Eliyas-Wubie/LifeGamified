from datetime import datetime

from src.models.domain.daily_report import DailyReport
from src.models.services import daily_report


def get_reports():
    domains = daily_report.get_all_reports()
    return domains


def make_report(data: dict):
    missions = data.get("completed_missions", [])
    compound_activities = (
        data.get("done_daily_activities", [])
        + data.get("done_uncomfortable_activities", [])
        + data.get("done_generic_activities", [])
    )
    domain = DailyReport(datetime.now(), compound_activities, missions)
    return daily_report.create_daily_report(domain)
