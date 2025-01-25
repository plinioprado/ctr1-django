from ledger1.document import documents

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_get_many_inv2_sell():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="inv2",
        doc_num=None)

    assert response["data"][0] == {
        'cpart_name': 'Cedar Store Ltd.',
        'descr': 'sale to cedar store ltd',
        'doc_dc': False,
        'doc_num': '1.1',
        'doc_type': 'inv2',
        'dt': '2020-01-20',
        'val': 1000.0
    }
    assert response['message'] == 'ok'
    assert response['status'] == 200


def test_get_many_inv2_buy():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=True,
        doc_type="inv2",
        doc_num=None)

    assert response["data"][0] == {
        'doc_type': 'inv2',
        'doc_num': '2.135',
        'doc_dc': True,
        'dt': '2020-01-05',
        'cpart_name': 'Jack Black',
        'descr': 'lawyer fees',
        'val': 200.0
    }
    assert response['message'] == 'ok'
    assert response['status'] == 200


def test_get_one_inv2_sell():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="inv2",
        doc_num="1.1")

    assert response['message'] == 'ok'
    assert response['status'] == 200
    assert response["data"] == {
        "descr": 'sale to cedar store ltd',
        "doc_type": "inv2",
        "doc_num": "1.1",
        "doc_dc": False,
        "dt": "2020-01-20",
        "seqs": [
            {
                "type": "base",
                "text": 'sale of services',
                "acc": "3.1.1",
                "val": 1000.0,
            },
            {
                "type": "add",
                "text": 'gst',
                "acc": "2.1.3",
                "val": 50.0,
            },
            {
                "type": "tot",
                "text": 'receivable',
                "acc": "1.1.3",
                "val": 1050.00
            }
        ],
        "fields": {
            "payment": {
                "account_num": "111222333",
                "institution_num": "003",
                "transit_num": "12345",
                "type": "eft"
            },
            "person": {
                "address": "333 Seymour st, suite 201",
                "city": "Vancouver",
                "country": "CAN",
                "name": "Cedar Store Ltd.",
                "pcode": "V6B5A6",
                "province": "BC"
            }
        },
    }


def test_get_new_inv2():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="inv2",
        doc_num="new")

    assert response['message'] == 'ok'
    assert response['status'] == 200
    assert response["data"] == {
        "descr": "",
        "doc_type": "inv2",
        "doc_num": "",
        "doc_dc": False,
        "dt": "",
        "seqs": [
            {"type": "base", "text": "", "acc": "", "val": 0.0},
            {"type": "tot", "text": "", "acc": "", "val": 0.0}
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


def test_post_inv2_sell():

    response = documents.post(
        api_key=API_KEY,
        doc_type="inv2",
        data={
            "doc_type": "inv2",
            "doc_num": "1.9",
            "doc_dc": False,
            "dt": "2020-01-22",
            "descr": "ddd",
            "fields": {
                "payment": {
                "account_num": "543211",
                "institution_num": "003",
                "transit_num": "55555",
                "type": "EFT"
                },
                "person": {
                "address": "101, Main st, suite 1001",
                "city": "Vancouver",
                "country": "Canada",
                "name": "Jack Black",
                "pcode": "V6E 1R1",
                "province": "BC"
                }
            },
            "seqs": [
                {
                "type": "base",
                "text": "",
                "acc": "3.1.1",
                "val": "10"
                },
                {
                "type": "tot",
                "text": "",
                "acc": "1.1.3",
                "val": 10
                }
            ]
        })

    assert response['message'] == "document inv2 1.9 created"
    assert response['status'] == 200

    response2 = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="inv2",
        doc_num="1.9")

    assert response2['data']["descr"] == "sale to Ccc Ltd"
