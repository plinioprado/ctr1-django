from ledger1.document.document1 import Document1
from ledger1.dao.sqlite import dao_document

def get(doc_type) -> dict:
    docs: list[Document1] = dao_document.get(doc_type)
    data = [ doc.asdict() for doc in docs]

    return {
        "code": 200,
        "message": "ok",
        "data": data
    }
