""" Ledger account crud

    Returns for all functions:
        dict: content of the REST response containing:
            code (int): 200 meaning success
            message (str): message
            data (lisr[dict]): list of dicts with account data, only applicable to GET
"""

from ledger1.account.account1 import Account1
import ledger1.dao.sqlite.account1_dao as dao

def get(acc: str, acc_to: str | None = None) -> dict:
    """ Get (read) accounts

    Arguments:
        acc: minimum account number to filter in format 9.9.9
        acc_to: maximum account number to filter in format 9.9.9,
            if None the filter will use the acc as maximum too
    """

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


def post(data: dict) -> dict:
    """ post (create) transaction

    Arguments:
        data: data of the account to be created as a dict
    """

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.post(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} created"
    }


def put(data: dict) -> dict:
    """ Put (update) account

    Arguments:
        data: data of the account to be updated as a dict
    """

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.put(acc)

    return {
        "code": 200,
        "message": f"account {acc_num} updated"
    }


def delete(acc_num: str) -> dict:
    """ Delete account

    Arguments:
        acc_num: number of the account to be deleted
    """

    if acc_num is None:
        raise ValueError("acc param missing")

    an = f"{acc_num[0:1]}.{acc_num[1:2]}.{acc_num[2:3]}"

    num: str = dao.delete(an)

    return {
        "code": 200,
        "message": f"account {num} deleted"
    }


def get_options() -> list[dict]:
    result = dao.get_options()

    return result
