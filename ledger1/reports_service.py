""" main service for reports """

from ledger1.util.settings import get as settings_get
from ledger1.util.fileio import write_csv
from ledger1.reports.chart_accounts import get as chart_accounts_get
from ledger1.reports.journal import get as journal_get
from ledger1.reports.general_ledger import get as general_ledger_get
from ledger1.reports.trial_balance import get as trial_balance_get


def service(name: str) -> dict:
    """ directs the request to its report service """

    # Get parameters
    settings = settings_get()
    entity_name = settings["entity"]["name"]
    date_from = settings["filters"]["date_from"]
    date_to = settings["filters"]["date_to"]

    # Get report
    if name == "chart_accounts":
        print(1)
        data: dict = chart_accounts_get(entity_name)
        print(2)
    elif name == "journal":
        data = journal_get(
            entity_name,
            date_from,
            date_to
        )
    elif name == "general_ledger":
        data = general_ledger_get(
            entity_name,
            date_from,
            date_to
        )
    elif name == "trial_balance":
        data = trial_balance_get(
            entity_name,
            date_from,
            date_to
        )
    else:
        raise ValueError("invalid report name")

    if data:
        export_csv(data)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def export_csv(data: dict) -> None:
    """ Save the report as csv file """

    rows = []
    for row in data["header"].values():
        rows.append([row])

    rows.append([])

    if "filters" in data:
        row = []
        for key in data["filters"].keys():
            row += [key, data["filters"][key]]
        rows.append(row)

    for row in data["table"]:
        rows.append(row)

    write_csv("./ledger1/file/report.csv", rows)
