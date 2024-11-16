""" Functions to handle requests to bank statement doucments

get_many() is only implemented for checking acc, therefore doc_dc == True
 """

from ledger1.document.banstat2 import Banstat2
from ledger1.admin import admin_service
from ledger1.reports import general_ledger
from ledger1.dao.sqlite import dao_document
from ledger1.utils import dateutil

def get(num: str = None) -> dict:
    if num is None:
        response = get_many()
    else:
        response = get_one(num)

    return response


def get_many() -> dict:
    ## obs: acc_num up to 11 dig
    doc_dc: bool = True

    data = dao_document.get_many("banstat2")

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_one(num: str, date: str = None, date_to: str = None):

    settings_date: list[dict] = admin_service.get_db_settings("field_date_")

    dt = dateutil.get_date_from(date, settings_date)
    dt_to = dateutil.get_date_to(date_to, settings_date)

    row = dao_document.get_one("banstat2", num)
    stat: Banstat2 = Banstat2()
    stat.set_from_db(row)
    tra_seqs: list[dict] = general_ledger.get(
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

    settings_db: list[dict] = admin_service.get_db_settings("institution_name_")
    institutions = []
    for setting in settings_db:
        institutions.append({
            "value": setting["key"].replace("institution_name_", ""),
            "text": setting["value"],
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
