""" Ledger account crud

    Returns for all functions:
        dict: content of the REST response containing:
            code (int): 200 meaning success
            message (str): message
            data (lisr[dict]): list of dicts with account data, only applicable to GET
"""

from ledger1.admin import entities
from ledger1.account.account1 import Account1
from ledger1.dao.sqlite import dao_account1

# get

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

    data = dao_account1.get(db_id, af, at)

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }


def get_many_by_doc(db_id: str, doc_type: str) -> list[dict]:

    data: list[dict] = dao_account1.get_many_by_doc(db_id, doc_type)

    return data


def get_one_by_doc(db_id: str, doc_type: str, doc_num: str) -> dict:

    data: dict = dao_account1.get_one_by_doc(db_id, doc_type, doc_num)

    return data


# post

def post(api_key: str, data: dict) -> dict:
    """ post (create) transaction

    Arguments:
        api_key: api key of the user
        data: data of the account to be created as a dict
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    acc_num = post_data(db_id, data)

    return {
        "code": 200,
        "message": f"account {acc_num} created"
    }


def post_data(db_id: str, data: dict) -> str:

    acc = Account1()
    acc.set_from_data(data)

    acc_num: str = dao_account1.post(db_id, acc)

    return acc_num


# put

def put(api_key: str, data: dict) -> dict:
    """ Put (update) account

    Arguments:
        api_key: api key of the user
        data: data of the account to be updated as a dict
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    acc_num: str = put_data(db_id, data)

    return {
        "code": 200,
        "message": f"account {acc_num} updated"
    }


def put_data(db_id: str, data: dict) -> str:

    acc = Account1()
    acc.set_from_data(data)

    acc_num: str = dao_account1.put(db_id, acc)

    return acc_num


# delete

def delete(api_key: str, acc_num: str) -> dict:
    """ Delete account

    Arguments:
    api_key: api key of the user
        acc_num: number of the account to be deleted
    """

    db_id: str = entities.get_db_id_by_api_key(api_key)

    deleted_num: str = delete_one(db_id, acc_num)

    return {
        "code": 200,
        "message": f"account {deleted_num} deleted"
    }


def delete_one(db_id: str, acc_num: str) -> dict:

    if acc_num is None:
        raise ValueError("acc param missing")

    if "." in acc_num:
        num: str = acc_num.replace(".", "")
    else:
        num = acc_num

    deleted_num: str = dao_account1.delete(db_id, num)

    return deleted_num


# helpers

def get_options(api_key) -> list[dict]:

    db_id: str = entities.get_db_id_by_api_key(api_key)

    result = dao_account1.get_options(db_id)

    return result
