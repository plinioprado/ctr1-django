""" main service for reports """

from ledger1.util.settings import get as settings_get
from ledger1.util.fileio import write_csv
from ledger1.reports.chart_accounts import get as chart_accounts_get
from ledger1.reports.journal import get as journal_get
from ledger1.reports.general_ledger import get as general_ledger_get
from ledger1.reports.trial_balance import get as trial_balance_get


def service(
        name: str,
        acc: str = None,
        acc_to: str = None,
        date: str = None,
        date_to: str = None
    ) -> dict:
    """ directs the request to its report service """

    # Get parameters
    settings = settings_get()
    entity_name = settings["entity"]["name"]
    af = settings["filters"]["acc_min"] if acc is None else f"{acc[0:1]}.{acc[1:2]}.{acc[2:3]}"
    at = settings["filters"]["acc_max"] if acc_to is None else f"{acc_to[0:1]}.{acc_to[1:2]}.{acc_to[2:3]}"
    df = settings["filters"]["date_min"] if date is None else date
    dt = settings["filters"]["date_max"] if date_to is None else date_to


    # Get report
    if name == "chart_accounts":
        data: dict = chart_accounts_get(
            entity_name,
            acc_from=af,
            acc_to=at
        )
    elif name == "journal":
        data = journal_get(
            entity_name,
            date_from=df,
            date_to=dt
        )
    elif name == "general_ledger":
        data = general_ledger_get(
            entity_name,
            date_from=df,
            date_to=dt,
            acc_from=af,
            acc_to=at
        )
    elif name == "trial_balance":
        data = trial_balance_get(
            entity_name,
            date_from=df,
            date_to=dt,
            acc_from=af,
            acc_to=at
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
