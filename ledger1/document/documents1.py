from ledger1.document.document1 import Document1
from ledger1.dao.sqlite import dao_document
from ledger1.utils.fileio import read_json

def get(doc_type: str, doc_num: str = None) -> dict:
    if doc_type is None and doc_num is None:
        raise ValueError("invalid document type")
    elif doc_num is None:
        res = get_many(doc_type)
    else:
        res = get_one(doc_type, doc_num)

    return res


def get_many(doc_type: str) -> dict:
    docs: list[Document1] = dao_document.get(doc_type)
    data = [ doc.asdict() for doc in docs]

    return {
        "code": 200,
        "data": data,
        "message": "ok",
    }

def get_one(doc_type: str, doc_num: str) -> dict:
    doc: Document1 = dao_document.get_one(doc_type, doc_num)
    data = doc.asdict()

    return {
        "code": 200,
        "data": data,
        "message": "ok",
    }
