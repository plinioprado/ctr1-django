from ledger1.utils import fileio
from ledger1.dao.sqlite import dao_document
from ledger1.document.document import Document
from ledger1.document import document_options
from ledger1.transaction import transaction_service as transactions
from ledger1.document.document_types import DocumentTypes

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

        doc: Document = get_document(doc_dc=doc_dc, doc_type=doc_type)
        data = doc.get_new()
        options = document_options.get(doc_type=doc_type, doc_dc=doc_dc)

        response = {
            "data": data,
            "message": "wip",
            "options": options,
            "status": 200,
        }

    else:
        options = document_options.get(doc_type=doc_type, doc_dc=doc_dc)

        data: dict = get_one(
            doc_dc=doc_dc,
            doc_type=doc_type,
            doc_num=doc_num,
            op_seq_acc=options["op_seq_acc"])

        response = {
            "data": data,
            "message": "wip",
            "options": options,
            "status": 200,
        }

    return response


def get_one(doc_dc: str, doc_type: str, doc_num: str, op_seq_acc: list[dict]):
    doc: Document = get_document(doc_dc=doc_dc, doc_type=doc_type)
    tra: dict = transactions.get_by_doc(doc_type, doc_num)
    doc.set_from_transaction(tra, op_seq_acc)

    res: dict = dao_document.get_one(doc_type, doc_num)
    doc.add_document_data(res)
    data = doc.get_to_response()

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

def post(doc_type: str, data) -> dict:
    options = document_options.get(doc_dc=data["doc_dc"], doc_type=data["doc_type"])

    doc: Document = get_document(doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc.set_from_request(data, options["op_seq_acc"])

    transactions.post(doc.get_to_transaction())
    dao_document.post(doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} created"
    }


# put


def put(doc_type: str, data: dict) -> dict:
    options = document_options.get(doc_dc=data["doc_dc"], doc_type=data["doc_type"])

    doc = get_document(doc_dc=data["doc_dc"], doc_type=doc_type)
    doc.set_from_request(data, options["op_seq_acc"])

    tra = transactions.get_by_doc(data["doc_type"], data["doc_num"])
    doc.tra_num = tra["num"]

    transactions.put(doc.get_to_transaction())
    dao_document.put(doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} updated"
    }


# delete


def delete(doc_type: str, doc_num: str) -> dict:

    tra = transactions.get_by_doc(doc_type, doc_num)
    transactions.delete(tra["num"])
    deleted_type, deleted_num = dao_document.delete(doc_type, doc_num)

    return {
        "status": 200,
        "message": f"document {deleted_type} {deleted_num} deleted"
    }


## helpers


# def get_op_seq_acc(doc_dc: bool, doc_type: str) -> list[dict]:
#     op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
#     options = [
#         op for op in op_seq_acc if op["doc_type"] == doc_type and (op["dc"] == "True") ==  doc_dc
#     ]

#     return options


def get_document(doc_dc: bool, doc_type: str) -> Document:
    document_type: dict = DocumentTypes().get(doc_type)

    return Document(doc_dc=doc_dc, document_type=document_type)
