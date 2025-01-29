""" main service for reports """

from ledger1.utils.settings import get as settings_file_get
from ledger1.utils.field import acc_num_is_valid
from ledger1.utils import dateutil
from ledger1.utils import fileio
from ledger1.admin import admin
from ledger1.admin import entities
from ledger1.reports.chart_accounts import get as chart_accounts_get
from ledger1.reports.journal import get as journal_get
from ledger1.reports.general_ledger import get as general_ledger_get
from ledger1.reports.trial_balance import get as trial_balance_get
from ledger1.reports.documents import get as documents_get


def service(
        name: str,
        api_key: str,
        acc: str = None,
        acc_to: str = None,
        date: str = None,
        date_to: str = None,
        doc_type: str = None
    ) -> dict:
    """ directs the request to its report service """

    # get entity name
    db_id: str = entities.get_db_id_by_api_key(api_key)
    entity_name: str = admin.get_db_settings(key="entity_name", db_id=db_id)["entity_name"]

    # for now, what is here should get from file settings
    settings = settings_file_get()

    # get date final
    if name == "chart_accounts":
        df = None
    if date is None:
        df = settings["filters"]["date_min"]
    elif not dateutil.date_iso_is_valid(date):
        raise ValueError(f"invalid date {date}")
    elif dateutil.date_iso_to_timestamp(date) < dateutil.date_iso_to_timestamp(settings["filters"]["date_min"]):
        raise ValueError(f"invalid date {date}: before min {settings["filters"]["date_min"]}")
    elif dateutil.date_iso_to_timestamp(date) > dateutil.date_iso_to_timestamp(settings["filters"]["date_max"]):
        raise ValueError(f"invalid date {date}: after max {settings["filters"]["date_max"]}")
    else:
        df = date

    if name == "chart_accounts":
        dt = None
    if date_to is None:
        dt = settings["filters"]["date_max"]
    elif not dateutil.date_iso_is_valid(date_to):
        raise ValueError(f"invalid date {date_to}")
    elif dateutil.date_iso_to_timestamp(date_to) < dateutil.date_iso_to_timestamp(settings["filters"]["date_min"]):
        raise ValueError(f"invalid date_to {date_to}: before min {settings["filters"]["date_min"]}")
    elif dateutil.date_iso_to_timestamp(date_to) > dateutil.date_iso_to_timestamp(settings["filters"]["date_max"]):
        raise ValueError(f"invalid date {date_to}: after max {settings["filters"]["date_max"]}")
    elif dateutil.date_iso_to_timestamp(date_to) < dateutil.date_iso_to_timestamp(date):
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
            db_id,
            entity_name,
            acc_from=af,
            acc_to=at
        )
    elif name == "journal":
        data = journal_get(
            db_id,
            entity_name,
            date_from=df,
            date_to=dt
        )
    elif name == "general_ledger":
        data = general_ledger_get(
            db_id,
            entity_name,
            date_from=df,
            date_to=dt,
            acc_from=af,
            acc_to=at
        )
    elif name == "trial_balance":
        data = trial_balance_get(
            db_id,
            entity_name,
            date_from=df,
            date_to=dt,
            acc_from=af,
            acc_to=at
        )
    elif name == "documents":
        data = documents_get(
            db_id,
            entity_name,
            date_from=df,
            date_to=dt,
            doc_type=doc_type
        )
    else:
        raise ValueError("invalid report name")

    if data:
        export_csv(data)

    res = {
        "code": 200,
        "message": "ok",
        "data": data
    }

    data_format: dict = get_format(name)
    if data_format is not None:
        res["format"] = data_format

    return res


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

    fileio.write_csv("./ledger1/file/report.csv", rows)


def get_format(name: str) -> dict:
    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]

    if name in ["chart_accounts","journal","general_ledger","trial_balance","documents"]:
        data_format: dict = fileio.read_json(f"{file_format_path}/rep_{name}_format.json")
    else:
        data_format = None

    return data_format
