""" Ledger transaction crud

    Returns for all functions:
        dict with content of the REST response containing:
            code (int): 200 meaning success
            message (str): message
            data (lisr[dict]): list of dicts with transaction data, only applicable to GET
"""

import ledger1.dao.sqlite.transaction1_dao as dao
from ledger1.transaction.transaction1 import Transaction1, Transaction1Seq
from ledger1.utils.settings import get as settings_get
from ledger1.account.account_service import get_options as get_options_acct
from ledger1.utils.field import date_iso_is_valid, date_iso_to_timestamp

def get(num: int | None,
        date: str = None,
        date_to: str = None) -> dict:
    """ get (read) transaction

    Arguments:
        num: number of the account to get
    """

    if num is None:
        response = get_many(date, date_to)

    elif num == 0:
        response = get_defaults()

    elif isinstance(num, int):
        response = get_one(int(num))
    else:
        raise ValueError("num invalid")

    return response


def post(data: dict) -> dict:
    """ post (create) transaction

    Arguments:
        data: data of the transaction to be created as a dict
    """

    seqs: list[Transaction1Seq] = [Transaction1Seq(
        seq=int(seq["seq"]),
        account=str(seq["account"]),
        val=float(seq["val"]),
        dc=bool(seq["dc"])) for seq in data["seqs"]]

    tra: Transaction1 = Transaction1(
        num=None,
        date=data["date"],
        descr=data["descr"],
        doc_type=data["doc_type"],
        doc_num=data["doc_num"],
        seqs=seqs
    )

    tra_num: int = dao.post(tra)

    return {
        "code": 200,
        "message": f"transaction {tra_num} created"
    }


def put(data: dict):
    """ put (update) transaction

    Arguments:
        data: data of the transaction to be updated as a dict
    """

    seqs: list[Transaction1Seq] = [Transaction1Seq(
        seq=int(seq["seq"]),
        account=str(seq["account"]),
        val=float(seq["val"]),
        dc=bool(seq["dc"])) for seq in data["seqs"]]

    tra: Transaction1 = Transaction1(
        num=data["num"],
        date=data["date"],
        descr=data["descr"],
        doc_type=data["doc_type"],
        doc_num=data["doc_num"],
        seqs=seqs
    )

    dao_num: int = dao.put(tra)

    return {
        "code": 200,
        "message": f"transaction {dao_num} updated"
    }


def delete(num: int):
    """ delete transaction

    Arguments:
        number of the account to delete
    """

    dao_num: int = dao.delete(num)

    return {
        "code": 200,
        "message": f"transaction {dao_num} deleted"
    }


def get_defaults():
    data: dict = {
        "num": None,
        "date": "",
        "descr": "",
        "doc_type": "",
        "doc_num": None,
        "seqs": []
    }
    options_account = get_options_acct()

    return {
        "code": 200,
        "message": "ok",
        "data": data,
        "options" : {
            "accounts": options_account
        }
    }


def get_one(num):
    result: Transaction1 | None = dao.get_one(num)

    data: dict = {} if result is None else result.asdict()
    options_account = None if not data else get_options_acct()
    options = {} if not options_account else { "accounts": options_account}

    return {
        "code": 200,
        "message": "ok",
        "data": data,
        "options": options
    }


def get_many(date: str, date_to: str):
    settings = settings_get()

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

    result: list[Transaction1] = dao.get_many(df, dt)
    data = []
    for tra in result:
        for seq in tra.seqs:

            data.append({
                "num": tra.num,
                "date": tra.date,
                "descr": tra.descr,
                "seq": seq.seq,
                "account": seq.account,
                "val": seq.val,
                "dc": seq.dc
            })

    return {
        "code": 200,
        "message": "ok",
        "data": data,
        "filters": {
            "date": df,
            "date_to": dt,
        },
    }
