from ledger1.document.document import Document

def test_get():
    doc_type = "eft"
    doc = Document(doc_type)

    assert doc.doc_type == "eft"
    assert doc.tra_seq == "new"

