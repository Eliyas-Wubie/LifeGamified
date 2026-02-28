from src.models.services import daily_report
def get_reports():
    domains=daily_report.get_all_reports()
    return domains