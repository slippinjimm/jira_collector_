import gspread
from jira_collector import get_json
from config import NAMES

GOOGLE_SHEET = f"Jira_issues"
GOOGLE_WORKSHEET = f"A worksheet"
PROJECT_NAME = f"FP"
FILTER_NAME = f"filter=10007"


def update_sheet(sheet_name: str, worksheetname: str, names: dict) -> None:
    gc = gspread.service_account()
    sh = gc.open(sheet_name)
    worksheet = sh.worksheet(worksheetname)
    json_dict = get_json(names, PROJECT_NAME, FILTER_NAME)
    columns_names = list(json_dict["FP-1"].keys())
    worksheet.update([columns_names], "A1:H1")
    values = []
    for values_list in list(json_dict.values()):
        values.append(list(values_list.values()))
    worksheet.update(values, "A2:H7")


def main() -> None:
    """schedule.every(10).seconds.do(update_sheet)
    while True:
        schedule.run_pending()
        time.sleep(1)"""
    update_sheet(GOOGLE_SHEET, GOOGLE_WORKSHEET, NAMES)


if __name__ == "__main__":
    main()
