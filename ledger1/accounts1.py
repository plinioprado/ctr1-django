""" Services for ledger account service """

from ledger1.models.account1 import Account1
import ledger1.dao.sqlite.account1_dao as dao

def get(acc: str, acc_to: str) -> list[dict]:
    """ Get (read) accounts """

    if acc is None:
        raise ValueError("acc param missing")

    af = f"{acc[0:1]}.{acc[1:2]}.{acc[2:3]}"
    at = af if acc_to is None else f"{acc_to[0:1]}.{acc_to[1:2]}.{acc_to[2:3]}"

    data = dao.get(af, at)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def post(data: dict) -> str:
    """ Port (create) account """

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.post(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} created"
    }


def put(data: dict) -> str:
    """ Put (update) account """

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.put(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} updated"
    }


def delete(acc: str) -> str:
    """ Delete account """

    if acc is None:
        raise ValueError("acc param missing")

    an = f"{acc[0:1]}.{acc[1:2]}.{acc[2:3]}"

    num: str = dao.delete(an)

    return {
        "code": 200,
        "message": f"account {num} deleted"
    }
