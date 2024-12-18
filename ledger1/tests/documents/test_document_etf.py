from ledger1.document.document import Document

def test_ini():
    doc = Document(
        doc_dc=True,
        document_type={
            "id": "eft",
            "name": "Eft",
            "num_on_seq": "base",
            "cpart_role_d": "",
            "cpart_role_c": "payee"
        })

    assert doc.doc_type == "eft"
    assert doc.doc_num == ""
    assert doc.doc_dc is True
    assert doc.tra_num == "new"
