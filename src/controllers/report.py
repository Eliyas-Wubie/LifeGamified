from src.models.services import daily_report
def get_reports():
    print("this is your report")
    domains=daily_report.get_all_reports()
    return domains