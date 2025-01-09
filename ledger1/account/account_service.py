""" Ledger account crud

    Returns for all functions:
        dict: content of the REST response containing:
            code (int): 200 meaning success
            message (str): message
            data (lisr[dict]): list of dicts with account data, only applicable to GET
"""

from ledger1.admin import entities
from ledger1.account.account1 import Account1
import ledger1.dao.sqlite.dao_account1 as dao

def get(
        api_key: str,
        acc: str,
        acc_to: str | None = None
    ) -> dict:
    """ Get (read) accounts

    Arguments:
        api_key: api key of the user
        acc: minimum account number to filter in format 9.9.9
        acc_to: maximum account number to filter in format 9.9.9,
            if None the filter will use the acc as maximum too
    """

    if acc is None:
        raise ValueError("acc param missing")

    af = f"{acc[0:1]}.{acc[1:2]}.{acc[2:3]}"
    at = af if acc_to is None else f"{acc_to[0:1]}.{acc_to[1:2]}.{acc_to[2:3]}"

    db_id: str = entities.get_db_id_by_api_key(api_key)

    db_id: str = entities.get_db_id_by_api_key(api_key)

    data = dao.get(db_id, af, at)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def post(api_key: str, data: dict) -> dict:
    """ post (create) transaction

    Arguments:
        api_key: api key of the user
        data: data of the account to be created as a dict
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.post(db_id, acc)

    return {
        "code": 200,
        "message": f"account {acc_num} created"
    }


def put(api_key: str, data: dict) -> dict:
    """ Put (update) account

    Arguments:
        api_key: api key of the user
        data: data of the account to be updated as a dict
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    acc = Account1(
        num=data["num"],
        name=data["name"],
        dc=data["dc"])

    acc_num: str = dao.put(db_id, acc)

    return {
        "code": 200,
        "message": f"account {acc_num} updated"
    }


def delete(api_key: str, acc_num: str) -> dict:
    """ Delete account

    Arguments:
    api_key: api key of the user
        acc_num: number of the account to be deleted
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    if acc_num is None:
        raise ValueError("acc param missing")

    an = f"{acc_num[0:1]}.{acc_num[1:2]}.{acc_num[2:3]}"

    num: str = dao.delete(db_id, an)

    return {
        "code": 200,
        "message": f"account {num} deleted"
    }


def get_options() -> list[dict]:
    result = dao.get_options()

    return result
