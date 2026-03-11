from src.models.services import accomplishment as accomplishment_service


def get_accomplishments():
    return accomplishment_service.view_accomplishments()
