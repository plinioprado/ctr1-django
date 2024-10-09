""" main service for reports """

from ledger1.utils.settings import get as settings_get
from ledger1.utils.fileio import write_csv
from ledger1.utils.field import date_iso_is_valid, date_iso_to_timestamp, acc_num_is_valid
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

    # Get and validate parameters
    settings = settings_get()

    entity_name = settings["entity"]["name"]

    if name == "chart_accounts":
        df = None
    if date is None:
        df = settings["filters"]["date_min"]
    elif not date_iso_is_valid(date):
        raise ValueError(f"invalid date {date}")
    elif date_iso_to_timestamp(date) < date_iso_to_timestamp(settings["filters"]["date_min"]):
        raise ValueError(f"invalid date {date}: before min {settings["filters"]["date_min"]}")
    elif date_iso_to_timestamp(date) > date_iso_to_timestamp(settings["filters"]["date_max"]):
        raise ValueError(f"invalid date {date}: after max {settings["filters"]["date_max"]}")
    else:
        df = date

    if name == "chart_accounts":
        dt = None
    if date_to is None:
        dt = settings["filters"]["date_max"]
    elif not date_iso_is_valid(date_to):
        raise ValueError(f"invalid date {date_to}")
    elif date_iso_to_timestamp(date_to) < date_iso_to_timestamp(settings["filters"]["date_min"]):
        raise ValueError(f"invalid date_to {date_to}: before min {settings["filters"]["date_min"]}")
    elif date_iso_to_timestamp(date_to) > date_iso_to_timestamp(settings["filters"]["date_max"]):
        raise ValueError(f"invalid date {date_to}: after max {settings["filters"]["date_max"]}")
    elif date_iso_to_timestamp(date_to) < date_iso_to_timestamp(date):
        raise ValueError("invalid date_to: before date")
    else:
        dt = date_to

    if acc is None:
        af: str = settings["filters"]["acc_min"]
    elif not acc_num_is_valid(f"{acc[0:1]}.{acc[1:2]}.{acc[2:]}"):
        raise f"invalid acc {acc}"
    else:
        af = f"{acc[0:1]}.{acc[1:2]}.{acc[2:3]}"

    if acc_to is None:
        at: str = settings["filters"]["acc_max"]
    elif not acc_num_is_valid(f"{acc_to[0:1]}.{acc_to[1:2]}.{acc_to[2:]}"):
        raise f"invalid acc {acc_to}"
    else:
        at = f"{acc_to[0:1]}.{acc_to[1:2]}.{acc_to[2:3]}"

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
