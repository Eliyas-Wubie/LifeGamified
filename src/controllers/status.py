from src.models.services import status as status_service

def get_profile():
    domain = status_service.get_player_profile()
    print("Get player called 🚒🚒")
    if domain:
        xp_rate: float | None = status_service.evaluate_xp_rate()
        print("xp_rate", xp_rate)
        domain.xp_rate = xp_rate if xp_rate is not None else 0
        return domain

def create_player(name:str):
    print("create player called 🚒🚒")
    return status_service.create_player(name)