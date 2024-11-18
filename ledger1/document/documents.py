from ledger1.utils import fileio
from ledger1.dao.sqlite import dao_document
from ledger1.document.document import Document
from ledger1.transaction import transaction_service as transactions

# get

def get(doc_dc: bool, doc_type: str = None, doc_num: str = None) -> dict:

    if doc_num is None:

        data: list[dict] = get_many(doc_dc, doc_type)

        response = {
            "data": data,
            "message": "wip",
            "status": 200,
        }
    elif doc_num == "new":
        doc = Document(doc_dc=doc_dc, doc_type=doc_type)
        data = doc.get_new()

        response = {
            "data": data,
            "message": "wip",
            "status": 200,
        }
    else:
        op_seq_acc = get_op_seq_acc(doc_dc)
        data: dict = get_one(
            doc_dc=doc_dc,
            doc_type=doc_type,
            doc_num=doc_num,
            op_seq_acc=op_seq_acc)

        response = {
            "data": data,
            "message": "wip",
            "status": 200,
        }

    return response


def get_one(doc_dc: str, doc_type: str, doc_num: str, op_seq_acc: list[dict]):
    pmt = Document(doc_dc=doc_dc, doc_type=doc_type)
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


def get_many(doc_dc: bool, doc_type: str):
    data = dao_document.get_many_tra(doc_dc=doc_dc, doc_type=doc_type)

    return data


# post



## helpers


def get_op_seq_acc(doc_dc: bool) -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
    options = [op for op in op_seq_acc if op["doc_type"] == "eft" and (op["dc"] == "True") ==  doc_dc]

    return options
