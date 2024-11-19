from ledger1.document import documents
from ledger1.admin import admin_service

admin_service.reset()

def test_get_many_eft_pay():
    response = documents.get(doc_dc=False, doc_type="eft", doc_num=None)
    assert response["data"][0] == {
        'cpart_name': 'Jack Black',
        'descr': 'pmt lawyer fees',
        'doc_dc': False,
        'doc_num': '1.1',
        'doc_type': 'eft',
        'dt': '2020-01-05',
        'val': 190.0,
    }
    assert response['message'] == 'wip'
    assert response['status'] == 200


def test_get_one_eft_pay():
    response = documents.get(doc_dc=False, doc_type="eft", doc_num=1.1)
    assert response["data"] == {
        "cpart_name": "Jack Black",
        "descr": "pmt lawyer fees",
        "doc_type": "eft",
        "doc_num": "1.1",
        "doc_dc": False,
        "dt": "2020-01-05",
        "seqs": [
            {
                "type": "base",
                "text": "account payable",
                "acc": "2.1.1",
                "val": 200.0
            },
            {
                "type": "sub",
                "text": "(-)discount on payment",
                "acc": "4.3.3",
                "val": 10.0
            },
            {
                "type": "tot",
                "text": "from acc 003.55555.7777777",
                "acc": "1.1.2",
                "val": 190.0
            }
        ],
    }
    assert response['message'] == 'wip'
    assert response['status'] == 200


def test_get_new_eft_pay():
    response = documents.get(doc_dc=False, doc_type="eft", doc_num="new")

    assert response['message'] == 'wip'
    assert response['status'] == 200
    assert response["data"] == {
        "doc_type": "eft",
        "doc_num": "",
        "doc_dc": False,
        "dt": "",
        "cpart_name": "",
        "descr": "",
        "tra_num": "new",
        "seqs": [
            {
                "type": "base",
                "text": "",
                "acc": "",
                "val": 0.0
            },
            {
                "type": "tot",
                "text": "",
                "acc": "",
                "val": 0.0
            }
        ]
    }


def test_post_eft_pay():

    response = documents.post(
        doc_type="eft",
        data={
            "doc_type": "eft",
            "doc_num": "1.99",
            "doc_dc": False,
            "dt": "2020-01-22",
            "cpart_name": "ccc",
            "descr": "some payment",
            "tra_num": "new",
            "seqs": [
                { "type": "base", "text": "", "acc": "2.1.1", "val": "100" },
                { "type": "tot", "text": "", "acc": "1.1.2", "val": 100 }
            ]
        })

    assert response['message'] == "document eft 1.99 created"
    assert response['status'] == 200

    response2 = documents.get(doc_dc=False, doc_type="eft", doc_num="1.99")

    assert response2['data']["descr"] == "some payment"


def test_put_eft_pay():

    response = documents.put(
        doc_type="eft",
        data={
            "doc_type": "eft",
            "doc_num": "1.99",
            "doc_dc": False,
            "dt": "2020-01-24",
            "cpart_name": "test Ltd.",
            "descr": "some payment2",
            "seqs": [
                {
                    "type": "base",
                    "text": "account payable",
                    "acc": "2.1.1",
                    "val": 111.00
                },
                {
                    "type": "tot",
                    "text": "from acc 003.55555.7777777",
                    "acc": "1.1.2",
                    "val": 111.00
                }
            ]

        })

    assert response['message'] == "document eft 1.99 updated"
    assert response['status'] == 200


    response2 = documents.get(doc_dc=False, doc_type="eft", doc_num="1.99")

    assert response2['data']["descr"] == "some payment2"


def test_delete_eft_pay():
    response = documents.delete(doc_type="eft", doc_num="1.99")

    assert response['message'] == "document eft 1.99 deleted"
    assert response['status'] == 200
