from ledger1.utils import fileio


def get(doc_type: str, doc_dc: bool):
    op_seq_acc = get_op_seq_acc(doc_dc, doc_type)

    return {
        "op_seq_acc": op_seq_acc
    }


def get_op_seq_acc(doc_dc: bool, doc_type: str) -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
    options = [
        op for op in op_seq_acc if op["doc_type"] == doc_type and (op["dc"] == "True") ==  doc_dc
    ]

    return options
