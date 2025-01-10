from ledger1.utils import fileio
from ledger1.document.document_types import DocumentTypes


def get_op_seq_acc(doc_dc: bool, doc_type: str) -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
    options = [
        op for op in op_seq_acc if op["doc_type"] == doc_type and (op["dc"] == "True") ==  doc_dc
    ]

    return options


def get_op_doc_dc(db_id: str, doc_type: str):

    document_type = DocumentTypes(db_id).get(doc_type=doc_type)
    options: list[dict] = [
        { "value": False, "text": document_type["dc_false_name"]},
        { "value": True, "text": document_type["dc_true_name"]}
    ]

    return options
