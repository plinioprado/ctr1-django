from ledger1.document.document import Document

def test_ini():
    doc_dc: bool = True
    op_seq_acc = {"id": "eft", "num_on_seq": "base"}
    doc = Document(doc_dc, op_seq_acc)

    assert doc.doc_type == "eft"
    assert doc.doc_num == ""
    assert doc.doc_dc == doc_dc
    assert doc.tra_num == "new"
