from ledger1.document import documents
from ledger1.admin import admin

admin.get(api_key="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p", param="reset")

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_get_many_eft_pay():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="eft",
        doc_num=None)

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
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="eft",
        doc_num=1.1)

    assert response["data"] == {
        "cpart_name": "Jack Black",
        "cpart_role": "Payer",
        "descr": "pmt lawyer fees",
        "doc_type": "eft",
        "doc_type_name": "EFT",
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
        "fields": {
            "payment": {
                "account_num": "222333444",
                "institution_num": "003",
                "transit_num": "23456",
                "type": "eft"
            },
            "person": {
                "address": "555, Burrard St, suite 1001",
                "city": "Vancouver",
                "country": "CAN",
                "name": "Jack Black",
                "pcode": "V7X1M8",
                "province": "BC"
            }
        },
    }
    assert response['message'] == 'wip'
    assert response['status'] == 200


def test_get_new_eft_pay():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="eft",
        doc_num="new")

    assert response['message'] == 'wip'
    assert response['status'] == 200
    assert response["data"] == {
        "doc_type": "eft",
        "doc_num": "",
        "doc_dc": False,
        "doc_type_name": "EFT",
        "dt": "",
        "cpart_name": "",
        "cpart_role": "Payer",
        "descr": "",
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
        ],
        "fields": {
            "payment": {
                "account_num": "",
                "institution_num": "",
                "transit_num": "",
                "type": ""
            },
            "person": {
                "address": "",
                "city": "",
                "country": "",
                "name": "",
                "pcode": "",
                "province": ""
            }
        }
    }


def test_post_eft_pay():

    response = documents.post(
        api_key=API_KEY,
        data={
            "doc_type": "eft",
            "doc_num": "1.99",
            "doc_dc": False,
            "dt": "2020-01-22",
            "cpart_name": "ccc",
            "descr": "some payment",
            "seqs": [
                { "type": "base", "text": "", "acc": "2.1.1", "val": 100 },
                { "type": "tot", "text": "", "acc": "1.1.2", "val": 100 }
            ]
        })

    assert response['message'] == "document eft 1.99 created"
    assert response['status'] == 200

    response2 = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="eft",
        doc_num="1.99")

    assert response2['data']["descr"] == "some payment"


def test_put_eft_pay():

    response = documents.put(
        api_key=API_KEY,
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


    response2 = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="eft",
        doc_num="1.99")

    assert response2['data']["descr"] == "some payment2"


def test_delete_eft_pay():
    response = documents.delete(
        api_key=API_KEY,
        doc_type="eft",
        doc_num="1.99")

    assert response['message'] == "document eft 1.99 deleted"
    assert response['status'] == 200
