# """ Functions to handle requests to bank statement doucments

# get_many() is only implemented for checking acc, therefore doc_dc == True
#  """

from ledger1.document.banstat2 import Banstat2
from ledger1.admin import admin
from ledger1.reports import general_ledger
from ledger1.dao.sqlite import dao_document
from ledger1.utils import dateutil
from ledger1.utils import fileio
from ledger1.admin import entities

def get(api_key: str, num: str = None) -> dict:

    if num is None:
        response = get_many(api_key)
    else:
        response = get_one(api_key, num)

    return response


def get_many(api_key: str) -> dict:
    ## obs: acc_num up to 11 dig

    db_id: str = entities.get_db_id_by_api_key(api_key)

    data = dao_document.get_many(db_id, "banstat2")

    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]
    data_format: dict = fileio.read_json(f"{file_format_path}/doc_banstats_format.json")

    return {
        "code": 200,
        "data": data,
        "format": data_format,
        "message": "ok"
    }


def get_one(api_key: str, num: str, date: str = None, date_to: str = None):

    db_id: str = entities.get_db_id_by_api_key(api_key)

    settings_date: dict = admin.get_db_settings("field_date_")
    dt = dateutil.get_date_from(date, settings_date)
    dt_to = dateutil.get_date_to(date_to, settings_date)

    row = dao_document.get_one(db_id, "banstat2", num)
    stat: Banstat2 = Banstat2()
    stat.set_from_db(row)
    tra_seqs: list[dict] = general_ledger.get(
        db_id,
        "",
        dt,
        dt_to,
        stat.acc_num,
        stat.acc_num)
    doc_seqs = []
    for tra_seq in tra_seqs["table"][2:]:
        doc_seqs.append({
            "dt": tra_seq[0],
            "descr": tra_seq[2],
            "cr": tra_seq[6],
            "db": tra_seq[7],
            "bal": tra_seq[8],
        })
    stat.set_seqs(doc_seqs)

    settings_db: list[dict] = admin.get_db_settings("institution_name_")

    institutions = []
    for key in settings_db.keys():
        institutions.append({
            "value": key.replace("institution_name_", ""),
            "text": settings_db[key],
        })
    options = {
        "institutions": institutions
    }

    return {
        "code": 200,
        "data": stat.toresult(),
        "options": options,
        "message": "ok"
    }
