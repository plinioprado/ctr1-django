from ledger1.document.document import Document

def test_ini():
    doc = Document(
        document_type={
            "id": "inv2",
            "name": "Invoice",
            "num_on_seq": "tot",
            "cpart_role_d": "",
            "cpart_role_c": "client"
        },
        doc_dc=True,
        doc_num="1.1"
    )

    assert doc.doc_type == "inv2"
    assert doc.doc_num == "1.1"
    assert doc.doc_dc is True
    assert doc.tra_num is None
