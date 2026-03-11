from src.models.services import profession as profession_service


def get_professions():
    return profession_service.view_professions()
