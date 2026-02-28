from src.models.services import status as status_service

def get_profile():
    domain = status_service.get_player_profile()
    if domain:
        xp_rate: float | None = status_service.evaluate_xp_rate()
        domain.xp_rate = xp_rate if xp_rate is not None else 0
        return domain

def create_player(name:str):
    return status_service.create_player(name)