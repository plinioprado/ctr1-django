""" Functions to handle requests to bank statement doucments """

from ledger1.document.banstat2 import Banstat2
from ledger1.dao.sqlite import dao_document

def get(num: str = None) -> dict:
    if num is None:
        response = get_many()
    else:
        response = get_one(num)

    return response


def get_many() -> dict:
    ## obs: acc_num up to 11 dig

    data = dao_document.get_many("banstat2")
    print(data)

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_one(num: str):

    stat: Banstat2 = Banstat2()

    return {
        "code": 200,
        "data": stat.toresult(),
        "message": "ok"
    }
