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
            "options": {
                "doc_dc": document_options.get_op_doc_dc(doc_type),
            },
            "filters": {
                "doc_dc": doc_dc
            }
        }

    elif doc_num == "new":

        doc: Document = get_document(doc_dc=doc_dc, doc_type=doc_type)
        data = doc.get_new()
        op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=doc_dc)

        response = {
            "data": data,
            "message": "wip",
            "options": {
                "op_seq_acc": op_seq_acc,
                "doc_dc": document_options.get_op_doc_dc(doc_type),
            },
            "status": 200,
        }

    else:
        tra: dict = transactions.get_by_doc(doc_type, doc_num)
        tra_doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]
        op_seq_acc = document_options.get_op_seq_acc(doc_type=doc_type, doc_dc=tra_doc_dc)

        doc: Document = get_document(doc_dc=tra_doc_dc, doc_type=doc_type)
        doc.set_from_transaction(tra, op_seq_acc)

        res: dict = dao_document.get_one(doc_type, doc_num)
        doc.add_document_data(res)
        data = doc.get_to_response()

        response = {
            "data": data,
            "message": "wip",
            "options": {
                "op_seq_acc": op_seq_acc,
                "doc_dc": document_options.get_op_doc_dc(doc_type),
            },
            "status": 200,
        }

    return response


def get_one(doc_type: str, doc_num: str, op_seq_acc: list[dict]):
    tra: dict = transactions.get_by_doc(doc_type, doc_num)
    doc_dc = [seq for seq in tra["seqs"] if seq["doc"]["type"] == doc_type][0]["dc"]

    doc: Document = get_document(doc_dc=doc_dc, doc_type=doc_type)

    doc.set_from_transaction(tra, op_seq_acc)

    res: dict = dao_document.get_one(doc_type, doc_num)
    doc.add_document_data(res)
    data = doc.get_to_response()

    return data


def get_many(doc_dc: bool, doc_type: str):
    data = dao_document.get_many_tra(doc_dc=doc_dc, doc_type=doc_type)

    return data


# post

def post(data) -> dict:
    op_seq_acc = document_options.get_op_seq_acc(doc_dc=data["doc_dc"], doc_type=data["doc_type"])

    doc: Document = get_document(doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc.set_from_request(data, op_seq_acc)

    transactions.post(doc.get_to_transaction())
    dao_document.post(doc.get_to_document())

    return {
        "status": 200,
        "message": f"document {data["doc_type"]} {data["doc_num"]} created"
    }


# put


def put(data: dict) -> dict:
    op_seq_acc = document_options.get_op_seq_acc(doc_dc=data["doc_dc"], doc_type=data["doc_type"])

    doc = get_document(doc_dc=data["doc_dc"], doc_type=data["doc_type"])
    doc.set_from_request(data, op_seq_acc)

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


def get_document(doc_dc: bool, doc_type: str) -> Document:
    document_type: dict = DocumentTypes().get(doc_type)

    return Document(doc_dc=doc_dc, document_type=document_type)
