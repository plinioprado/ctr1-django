from ledger1.document import documents


def test_get_many_inv2_sell():
    response = documents.get(doc_dc=False, doc_type="inv2", doc_num=None)
    assert response["data"][0] == {
        'cpart_name': 'Cedar Store Ltd',
        'descr': 'sale to cedar store ltd',
        'doc_dc': False,
        'doc_num': '1.1',
        'doc_type': 'inv2',
        'dt': '2020-01-20',
        'val': 1000.0
    }
    assert response['message'] == 'wip'
    assert response['status'] == 200


def test_get_many_inv2_buy():
    response = documents.get(doc_dc=True, doc_type="inv2", doc_num=None)
    assert response["data"][0] == {
        'doc_type': 'inv2',
        'doc_num': '2.135',
        'doc_dc': True,
        'dt': '2020-01-05',
        'cpart_name': 'Jack Black',
        'descr': 'lawyer fees',
        'val': 200.0
    }
    assert response['message'] == 'wip'
    assert response['status'] == 200


def test_get_one_inv2_sell():
    response = documents.get(doc_dc=False, doc_type="inv2", doc_num=1.1)

    assert response['message'] == 'wip'
    assert response['status'] == 200
    assert response["data"] == {
        "cpart_name": "Cedar Store Ltd",
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
    }


def test_get_new_inv2():
    response = documents.get(doc_dc=False, doc_type="inv2", doc_num="new")

    assert response['message'] == 'wip'
    assert response['status'] == 200
    assert response["data"] == {
        "doc_type": "inv2",
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


def test_post_inv2_sell():

    response = documents.post(
        doc_type="eft",
        data={
            "doc_type": "inv2",
            "doc_num": "9.1",
            "doc_dc": False,
            "dt": "2020-01-22",
            "cpart_name": "Ccc Ltd",
            "descr": "sale to Ccc Ltd",
            "tra_num": "new",
            "seqs": [
                { "type": "base", "text": "", "acc": "3.1.1", "val": 100 },
                { "type": "add", "text": "", "acc": "2.1.3", "val": 5 },
                { "type": "tot", "text": "", "acc": "1.1.3", "val": 105 }
            ]
        })

    assert response['message'] == "document eft 9.1 created"
    assert response['status'] == 200

    response2 = documents.get(doc_dc=False, doc_type="inv2", doc_num="9.1")

    assert response2['data']["descr"] == "some payment"
