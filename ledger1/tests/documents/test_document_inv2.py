from ledger1.document.document import Document

def test_ini():
    op_seq_acc = {"id": "inv2", "num_on_seq": "tot"}
    doc_dc: bool = True
    doc = Document(doc_dc, op_seq_acc)

    assert doc.doc_type == "inv2"
    assert doc.doc_num == ""
    assert doc.doc_dc is True
    assert doc.tra_num == "new"
