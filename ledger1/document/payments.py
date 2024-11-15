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

from ledger1.dao.sqlite import dao_document
from ledger1.document.payment import Payment
from ledger1.transaction import transaction_service as transactions
from ledger1.utils import fileio

def get(doc_type: str = None, doc_num: str = None):
    if doc_num is None:
        response = {
            "data": get_many(),
            "message": "ok",
            "code": 200,
        }
    else:
        op_seq_acc = get_op_seq_acc()
        response = {
            "data": get_one(doc_type, doc_num, op_seq_acc),
            "message": "ok",
            "options": {
                "doc_seq_acc": op_seq_acc
            },
            "code": 200,
        }

    return response


def get_many():
    data: list[dict] = [{
            "doc_type": "eft",
            "doc_num": "1.1",
            "doc_dc": True,
            "dt": "2020-01-05",
            "cpart_name": "Jack Black",
            "descr": "Pmt for legal fees",
            "val": 200
        }
    ]

    return data


def get_one(doc_type: str, doc_num: str, op_seq_acc: list[dict]):
    pmt = Payment()
    tra = transactions.get_by_doc(doc_type, doc_num)
    pmt.set_from_transaction(tra, op_seq_acc)

    doc: dict = dao_document.get_one(doc_type, doc_num)
    pmt.add_document_data(doc)

    data = pmt.get_to_response()
    return data

def get_op_seq_acc() -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc.csv')
    options = [op for op in op_seq_acc if op["doc_type"] == "eft" and op["dc"] == "1"]

    return options
