from ledger1.document.document import Document

def test_ini():
    doc = Document(
        doc_dc=True,
        document_type={
            "id": "inv2",
            "name": "Invoice",
            "num_on_seq": "tot",
            "cpart_role_d": "",
            "cpart_role_c": "client"
        }
    )

    assert doc.doc_type == "inv2"
    assert doc.doc_num == ""
    assert doc.doc_dc is True
    assert doc.tra_num == "new"
