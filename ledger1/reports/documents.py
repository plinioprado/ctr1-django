""" business logic to create the documents report """

from ledger1.document.document_types import DocumentTypes
from ledger1.dao.sqlite.dao_report import get_documents

def get(
    db_id: str,
    entity_name: str,
    date_from: str,
    date_to: str,
    doc_type: str = ""
) -> dict:

    document_types = DocumentTypes()
    options_doc_type = document_types.get_dict_options()

    rows: list[dict] = get_documents(
            db_id,
            date_from,
            date_to,
            doc_type
        )

    return {
        "header": {
            "entity_name": entity_name,
            "title": "documents",
        },
        "filters": {
            "doc_type": doc_type,
            "date": date_from,
            "date_to": date_to
        },
        "options": {
            "doc_type": options_doc_type
        },
        "table": rows,
    }
