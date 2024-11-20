from ledger1.utils import fileio


def get_op_seq_acc(doc_dc: bool, doc_type: str) -> list[dict]:
    op_seq_acc = fileio.read_csv('./ledger1/dao/csv/document_acc_type.csv')
    options = [
        op for op in op_seq_acc if op["doc_type"] == doc_type and (op["dc"] == "True") ==  doc_dc
    ]

    return options


def get_op_doc_dc(doc_type: str):

    if doc_type == "inv2":
        options: list[dict] = [
            { "value": False, "text": "Sell"},
            { "value": True, "text": "Buy"}
        ]
    else:
        options = [{ "value": True, "text": "Pay"}]

    return options
