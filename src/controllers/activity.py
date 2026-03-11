from src.models.domain.activity import CompoundActivity
from src.models.services import activity as activity_service


def get_compound_activities():
    return activity_service.view_compound_activities()


def get_daily_activities():
    return activity_service.view_compound_activities(tag="daily")


def get_uncomfortable_activities():
    return activity_service.view_compound_activities(tag="discomfort")


def get_generic_activities():
    return activity_service.view_compound_activities(tag="generic")


def create_compound_activity(data: dict):
    name = (data.get("name") or "").strip()
    xp = float(data.get("xp") or 0)
    domain = CompoundActivity(name, xp, [])
    return activity_service.update_compound_activity(domain)


def delete_compound_activity(item: CompoundActivity):
    return activity_service.delete_compound_activity(item)
