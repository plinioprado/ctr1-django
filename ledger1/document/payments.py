"""
Payment feature handles payments and receivings

Attributes:
    doc_dc: True if Payment and False if Receiving
    doc_type : eft, cheque..., will drive the primary fields - TODO
    doc_num: unique identifier for that type

For get_one, doc_dc is not required because the doc_num structure: {person_num}.{doc_id}.
"""


from ledger1.dao.sqlite import dao_document
from ledger1.document.payment import Payment
from ledger1.transaction import transaction_service as transactions
from ledger1.utils import fileio

def get(doc_dc: bool, doc_type: str = None, doc_num: str = None):
    if doc_num is None:
        response = {
            "data": get_many(doc_dc),
            "message": "ok",
            "code": 200,
        }
    elif doc_num == "new":
        op_seq_acc = get_op_seq_acc(doc_dc)
        response = {
            "data": get_new(doc_dc),
            "message": "ok",
            "options": {
                "doc_seq_acc": op_seq_acc
            },
            "code": 200,
        }
    else:
        op_seq_acc = get_op_seq_acc(doc_dc)
        data = get_one(doc_type, doc_num, op_seq_acc)

        response = {
            "data": data,
            "message": "ok",
            "options": {
                "doc_seq_acc": op_seq_acc
            },
            "code": 200,
        }

    return response


def get_many(doc_dc: bool):
    data = dao_document.get_many_tra(doc_dc=doc_dc, doc_type="eft")

    return data


def get_one(doc_type: str, doc_num: str, op_seq_acc: list[dict]):
    pmt = Payment()
    tra: dict = transactions.get_by_doc(doc_type, doc_num)
    pmt.set_from_transaction(tra, op_seq_acc)

    doc: dict = dao_document.get_one(doc_type, doc_num)
    pmt.add_document_data(doc)
    data = pmt.get_to_response()

    # Because initially doc_type was in doc.seqs[0]
    if data["doc_type"] != doc_type:
        data["doc_type"] = doc_type
        data["doc_num"] = doc_num
        data["doc_dc"] = False

    return data


def get_new(doc_dc: bool):
    return {
        "doc_type": "eft",
        "doc_num": "",
        "doc_dc": doc_dc,
        "dt": "",
        "cpart_name": "",
        "descr": "",
        "tra_num": "new",
        "seqs": [
            {
                "type": "base",
                "text": "",
                "acc": "",
                "val": 0.0
            },
            {
                "type": "tot",
                "text": "",
                "acc": "",
                "val": 0.0
            }
        ]
    }


def get_op_seq_acc(doc_dc: bool) -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
    options = [op for op in op_seq_acc if op["doc_type"] == "eft" and (op["dc"] == "True") ==  doc_dc]

    return options


def post(data) -> dict:
    """ create new payment """
    pmt: Payment = Payment()
    op_seq_acc = get_op_seq_acc(False)
    pmt.set_from_request(data, op_seq_acc)
    transactions.post(pmt.get_to_transaction())
    dao_document.post(pmt.get_to_document())

    return {
        "code": 200,
        "message": f"document  {data["doc_type"]} {data["doc_num"]} created"
    }


def put( data: dict) -> dict:
    """ create new payment """

    pmt: Payment = Payment()
    op_seq_acc = get_op_seq_acc(False)

    pmt.set_from_request(data, op_seq_acc)
    tra = transactions.get_by_doc(data["doc_type"], data["doc_num"])
    pmt.tra_num = tra["num"]

    transactions.put(pmt.get_to_transaction())
    dao_document.put(pmt.get_to_document())

    return {
        "code": 200,
        "message": f"document  {data["doc_type"]} {data["doc_num"]} updated"
    }


def delete(doc_type: str, doc_num: str) -> dict:

    tra = transactions.get_by_doc(doc_type, doc_num)
    transactions.delete(tra["num"])
    deleted_type, deleted_num = dao_document.delete(doc_type, doc_num)

    return {
        "code": 200,
        "message": f"document {deleted_type} {deleted_num} deleted"
    }
