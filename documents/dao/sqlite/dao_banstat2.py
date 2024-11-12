
def get_one_header(num):

    data: list[dict] = {
        "num": num,
        "institution": "003 - RBC",
        'transit_num': "55555",
        "acc_num": "7777777",
        "descr": "rbc 55555-7777777 account",
        "acct": "1.1.2"
    }

    return data


def get_one_seqs(acct):

    data = [{
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


    return data


