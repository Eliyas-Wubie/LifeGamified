from src.models.services import status as status_service


def get_attributes():
    return status_service.view_attributes()
