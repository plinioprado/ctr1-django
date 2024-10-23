""" test of transactions crud """

# pylint: disable=missing-function-docstring

import ledger1.transaction.transaction_service as service
from ledger1.utils.dbutil import reset_db

def test_get():

    reset_db()

    result = service.get(1)

    assert result["code"] == 200
    assert result["message"] == "ok"
    assert result["data"] == {
        'num': 1,
        'date': "2020-01-02",
        'descr': "capital contribution",
        "doc_type": "statement1",
        "doc_num": 1,
        "seqs": [
            {
                "seq": 1,
                "account": "1.1.2",
                "val": 10000.,
                "dc": True
            },
            {
                "seq": 2,
                "account": "2.3.1",
                "val": 10000.,
                "dc": False
            }
        ]
    }
    assert result["options"]["accounts"][0] == {'text': 'assets', 'value': '1.0.0'}


    result = service.get(999)

    assert result == {
            "code": 200,
        "message": "ok",
        "data": {},
        "options": {}
    }


def test_post():

    result = service.post({
            "date": "2020-01-25",
            "descr": "sale to test ltd",
            "doc_type": "invoice1",
            "doc_num": 2,
            "seqs": [
                {
                    "seq": 1,
                    "account": "3.1.1",
                    "val": 1000.,
                    "dc": True
                },
                {
                    "seq": 2,
                    "account": "1.1.3",
                    "val": 1000.,
                    "dc": False
                }
            ]
        })

    assert result == {
        "code": 200,
        "message": "transaction 5 created"
    }

    result2 = service.get(5)

    assert result2["code"] == 200
    assert result2["message"] == "ok"
    assert result2["data"] == {
            "num": 5,
            "date": "2020-01-25",
            "descr": "sale to test ltd",
            "doc_type": "invoice1",
            "doc_num": 2,
            "seqs": [
                {
                    "seq": 1,
                    "account": "3.1.1",
                    "val": 1000.,
                    "dc": True
                },
                {
                    "seq": 2,
                    "account": "1.1.3",
                    "val": 1000.,
                    "dc": False
                }
            ]
        }


def test_update():

    result = service.put({
        "num": 5,
        "date": "2020-01-25",
        "descr": "sale to test ltdxxx",
        "doc_type": "invoice1",
        "doc_num": 2,
        "seqs": [
            {
                "seq": 1,
                "account": "3.1.1",
                "val": 1001.,
                "dc": True
            },
            {
                "seq": 2,
                "account": "1.1.3",
                "val": 1001.,
                "dc": False
            }
        ]
    })

    assert result == {
        "code": 200,
        "message": "transaction 5 updated"
    }

    result2 = service.get(5)

    assert result2["code"] == 200
    assert result2["message"] == "ok"
    assert result2["data"] == {
        "num": 5,
        "date": "2020-01-25",
        "descr": "sale to test ltdxxx",
        "doc_type": "invoice1",
        "doc_num": 2,
        "seqs": [
            {
                "seq": 1,
                "account": "3.1.1",
                "val": 1001.,
                "dc": True
            },
            {
                "seq": 2,
                "account": "1.1.3",
                "val": 1001.,
                "dc": False
            }
        ]}


def test_delete():

    result = service.delete(5)

    assert result == {
        "code": 200,
        "message": "transaction 5 deleted"
    }

    result2 = service.get(5)

    assert result2 == {
        "code": 200,
        "message": "ok",
        "data": {},
        "options": {}
    }
