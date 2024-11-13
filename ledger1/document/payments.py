"""
Payment is any money transfer from or to the tenant

Attributes:
    doc_type: 'pmt'
    doc_subtype : eft, cheque..., will drive the primary fields - TODO
    doc_num: unique identifier for that type
    doc_dc: True (debit) if made or  False (credit) if received
    dt: date of the sending (for now assumed to be the same of the receiving)
    descr: description
    tra_num: number of the transaction
    doc_seqs:
        debits and credits related, with the respective types, accounts and amounts
"""

def get(num: str = None):
    if num is None:
        data = get_many()
    else:
        data = get_one(num)

    return {
        "data": data,
        "message": "ok",
        "code": 200,
    }


def get_many():
    data: list[dict] = [{
            "doc_type": "pmt",
            "doc_num": "1.1",
            "doc_dc": True,
            "dt": "2020-01-05",
            "cpart_name": "Jack Black",
            "descr": "Pmt for legal fees",
            "val": 200
        }
    ]

    return data


def get_one(num: str):
    data: dict = {
            "doc_type": "eft",
            "doc_num": num,
            "doc_dc": True,
            "dt": "2020-01-05",
            "cpart_name": "Jack Black",
            "descr": "Pmt for legal fees",
            "tra_num": 2,
            "seqs": [
                {
                    "type": "base",
                    "text": "from acc 003.55555.7777777",
                    "acc": "1.1.2",
                    "val": 200.00,
                },
                {
                    "type": "tot",
                    "text": "to admin.expense",
                    "acc": "1.1.2",
                    "val": 200.00,
                }
            ]
        }

    return data
