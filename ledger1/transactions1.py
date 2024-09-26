""" Transactions 1 CRUD """

import ledger1.dao.sqlite.transaction1_dao as dao
from ledger1.models.transaction1 import Transaction1, Transaction1Seq

def get(num: str) -> dict:
    """ get (read) transaction """

    result: Transaction1 | None = dao.get(num)

    data = {} if result is None else result.asdict()

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def post(data: dict) -> dict:
    """ post (create) transaction """

    seqs = [Transaction1Seq(
        seq=int(seq["seq"]),
        account=str(seq["account"]),
        val=float(seq["val"]),
        dc=bool(seq["dc"])) for seq in data["seqs"]]

    tra = Transaction1(
        num=None,
        date=data["date"],
        descr=data["descr"],
        doc_type=data["doc_type"],
        doc_num=data["doc_num"],
        seqs=seqs
    )

    tra_num = dao.post(tra)

    return {
        "code": 200,
        "message": f"transaction {tra_num} created"
    }


def put(data: dict):
    """ put (update) transaction """

    seqs = [Transaction1Seq(
        seq=int(seq["seq"]),
        account=str(seq["account"]),
        val=float(seq["val"]),
        dc=bool(seq["dc"])) for seq in data["seqs"]]

    tra = Transaction1(
        num=data["num"],
        date=data["date"],
        descr=data["descr"],
        doc_type=data["doc_type"],
        doc_num=data["doc_num"],
        seqs=seqs
    )

    dao_num = dao.put(tra)

    return {
        "code": 200,
        "message": f"transaction {dao_num} updated"
    }


def delete(num: int):
    """ delete transaction """

    dao_num = dao.delete(num)

    return {
        "code": 200,
        "message": f"transaction {dao_num} deleted"
    }
