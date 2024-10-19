""" Ledger transaction crud

    Returns for all functions:
        dict with content of the REST response containing:
            code (int): 200 meaning success
            message (str): message
            data (lisr[dict]): list of dicts with transaction data, only applicable to GET
"""

import ledger1.dao.sqlite.transaction1_dao as dao
from ledger1.transaction.transaction1 import Transaction1, Transaction1Seq

def get(num: int) -> dict:
    """ get (read) transaction

    Arguments:
        num: number of the account to get
    """

    if num is None:
        result: list[Transaction1] = dao.get_many()
        data = []
        for tra in result:
            for seq in tra.seqs:

                data.append({
                    "num": tra.num,
                    "date": tra.date,
                    "descr": tra.descr,
                    "account": seq.account,
                    "val": seq.val,
                    "dc": seq.dc
                })

        response = {
            "code": 200,
            "message": "ok",
            "data": data,
            "filters": {
                "date": "2020-01-01",
                "date_to": "2020-01-31",
            },
        }

    else:
        result: Transaction1 | None = dao.get_one(num)
        data: dict = {} if result is None else result.asdict()

        response = {
            "code": 200,
            "message": "ok",
            "data": data
        }

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
