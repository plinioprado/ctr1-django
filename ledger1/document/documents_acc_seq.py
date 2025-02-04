from ledger1.transaction import transactions
from ledger1.utils import dateutil

def get(db_id: int, acc_num: str) -> list[dict]:
    print(1, db_id, acc_num)

    tras: list[dict] = transactions.get_by_acc(db_id, acc_num)
    # {'num': 2, 'date': 1577923200.0, 'descr': 'capital contribution jane doe', 'seq': 1, 'account_num': '1.1.2', 'val': 10000.0, 'dc': 1, 'doc_type': '', 'doc_num': ''}

    seqs = []
    bal: float = 0
    for tra in tras:
        bal += tra["val"] if tra["dc"] == 1 else -tra["val"]
        seqs.append({
            "date": dateutil.date_timestamp_to_iso(tra["date"]),
            "descr": tra["descr"],
            "db": tra["val"] if tra["dc"] == 1 else 0,
            "cr": tra["val"] if tra["dc"] == 0 else 0,
            "bal": bal,
            "doc_type": tra["doc_type"],
            "doc_num": tra["doc_num"]
        })

    return seqs


    # return [
    #     {
    #         "date": "2021-01-01",
    #         "descr": "Opening balance",
    #         "db": 0,
    #         "cr": 0,
    #         "bal": 0
    #     },
    #     {
    #         "date": "2021-01-02",
    #         "descr": "capital contribution john doe",
    #         "db": 0,
    #         "cr": 10000,
    #         "bal": 100000
    #     }]
