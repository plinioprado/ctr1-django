""" Services for ledger account service """

from ledger1.models.account1 import Account1
import ledger1.dao.sqlite.account1_dao as dao

def get(acc_from: str, acc_to: str) -> list[dict]:
    """ Get (read) accounts """

    data = dao.get(acc_from, acc_to)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def post(acc: Account1) -> str:
    """ Port (create) account """

    acc_num: str = dao.post(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} created"
    }


def put(acc: Account1) -> str:
    """ Put (update) account """

    acc_num: str = dao.put(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} updated"
    }


def delete(acc_num: str) -> str:
    """ Delete account """

    num: str = dao.delete(acc_num)

    return {
        "code": 200,
        "message": f"account {num} deleted"
    }
