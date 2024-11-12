""" Functions to handle requests to bank statement doucments """

from ledger1.document.banstat2 import Banstat2

def get(num: str = None) -> dict:
    if num is None:
        response = get_many()
    else:
        response = get_one(num)

    return response


def get_many() -> dict:
    ## obs: acc_num up to 11 dig

    data: list[dict] = [
            {
                "num": 1,
                "institution": "003 - RBC",
                'transit_num': "55555",
                "acc_num": "7777777",
                "descr": "rbc 55555-7777777 account",
            },
        ]

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
