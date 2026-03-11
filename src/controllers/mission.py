from src.models.domain.mission import Mission
from src.models.services import mission as mission_service


def get_missions():
    return mission_service.view_missions()


def create_mission(data: dict):
    name = (data.get("name") or "").strip()
    description = data.get("description")
    deadline = data.get("deadline")
    domain = Mission(name, description, deadline)
    return mission_service.update_mission(domain)


def delete_mission(item: Mission):
    return mission_service.delete_mission(item)
