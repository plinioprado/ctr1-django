from ledger1.document.document import Document

def test_get():
    doc_type = "inv"
    doc = Document(doc_type)

    assert doc.doc_type == "inv"
    assert doc.tra_seq == "new"
