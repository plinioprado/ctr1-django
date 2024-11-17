from ledger1.document.document import Document

def test_get():
    doc_type = "eft"
    doc_dc: bool = True
    doc = Document(doc_type, doc_dc)

    assert doc.doc_type == "eft"
    assert doc.doc_num == ""
    assert doc.doc_dc == doc_dc
    assert doc.tra_num == "new"
