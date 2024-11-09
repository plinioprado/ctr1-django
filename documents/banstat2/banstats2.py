""" Functions to handle requests to bank statement doucments """

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
            {
                "num": 2,
                "institution": "001 - BMO",
                'transit_num': "12345",
                "acc_num": "1234567",
                "descr": "td 12345-1234567 account",
            }
        ]

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }


def get_one(num: str):
    data = {
        "num": num,
        "institution": "003 - RBC",
        'transit_num': "55555",
        "acc_num": "7777777",
        "descr": "rbc 55555-7777777 account",
        "seqs": [
            {
                "dt": "2020-01-02",
                "descr": "opening balance",
                "db": 0,
                "cr": 0,
                "bal": 0
            },
            {
                "dt": "2020-01-02",
                "descr": "capital contribution",
                "cr": 10000,
                "db": 200,
                "bal": 10000
            },
                        {
                "dt": "2020-01-05",
                "descr": "lawyer fees",
                "cr": 0,
                "db": 200,
                "bal": 9800
            },
            {
                "dt": "2020-01-21",
                "descr": "receiving from cedar store ltd",
                "cr": 0,
                "db": 11050,
                "bal": 10850
            }
        ]
    }

    return {
        "code": 200,
        "data": data,
        "message": "ok"
    }
