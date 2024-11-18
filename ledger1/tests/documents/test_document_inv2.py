from ledger1.document.document import Document

def test_ini():
    doc_type: str = "inv2"
    doc_dc: bool = True
    doc = Document(doc_type, doc_dc)

    assert doc.doc_type == "inv2"
    assert doc.doc_num == ""
    assert doc.doc_dc is True
    assert doc.tra_num == "new"
