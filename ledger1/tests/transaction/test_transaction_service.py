""" test of transactions crud """

# pylint: disable=missing-function-docstring

import ledger1.transaction.transaction_service as service
from ledger1.admin import admin
from ledger1.tests.utils import test_util

next_num = test_util.get_last_tra_num() + 1


def test_get_one():

    admin.get("reset")

    result = service.get(1)

    assert result["code"] == 200
    assert result["message"] == "ok"
    assert result["data"] == {
        'num': 1,
        'date': "2020-01-02",
        'descr': "capital contribution john doe",
        "seqs": [
            {
                "account": "1.1.2",
                "val": 10000.,
                "dc": True,
                "doc": {
                    "type": "",
                    "num": "",
                }
            },
            {
                "account": "2.3.1",
                "val": 10000.,
                "dc": False,
                "doc": {
                    "type": "",
                    "num": ""
                }
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
            "seqs": [
                {
                    "account": "3.1.1",
                    "val": 1000.,
                    "dc": True,
                    "doc": {
                        "type": "",
                        "num": "",
                    }
                },
                {
                    "account": "1.1.3",
                    "val": 1000.,
                    "dc": False,
                    "doc": {
                        "type": "",
                        "num": "",
                    }
                }
            ]
        })

    assert result == {
        "code": 200,
        "data": { "id": next_num },
        "message": f"transaction {next_num} created"
    }

    result2 = service.get(next_num)

    assert result2["code"] == 200
    assert result2["message"] == "ok"
    assert result2["data"] == {
            "num": next_num,
            "date": "2020-01-25",
            "descr": "sale to test ltd",
            "seqs": [
                {
                    "account": "3.1.1",
                    "val": 1000.,
                    "dc": True,
                    "doc": {
                        "type": "",
                        "num": "",
                    }
                },
                {
                    "account": "1.1.3",
                    "val": 1000.,
                    "dc": False,
                    "doc": {
                        "type": "",
                        "num": "",
                    }
                }
            ]
        }


def test_update():

    result = service.put({
        "num": next_num,
        "date": "2020-01-25",
        "descr": "sale to test ltdxxx",
        "seqs": [
            {
                "account": "3.1.1",
                "val": 1001.,
                "dc": True,
                "doc": {
                    "type": "",
                    "num": "",
                }
            },
            {
                "account": "1.1.3",
                "val": 1001.,
                "dc": False,
                "doc": {
                    "type": "",
                    "num": "",
                }
            }
        ]
    })

    assert result == {
        "code": 200,
        "message": f"transaction {next_num} updated"
    }

    result2 = service.get(next_num)

    assert result2["code"] == 200
    assert result2["message"] == "ok"
    assert result2["data"] == {
        "num": next_num,
        "date": "2020-01-25",
        "descr": "sale to test ltdxxx",
        "seqs": [
            {
                "account": "3.1.1",
                "val": 1001.,
                "dc": True,
                "doc": {
                    "type": "",
                    "num": "",
                }
            },
            {
                "account": "1.1.3",
                "val": 1001.,
                "dc": False,
                "doc": {
                    "type": "",
                    "num": "",
                }
            }
        ]}


def test_delete():

    result = service.delete(next_num)

    assert result == {
        "code": 200,
        "message": f"transaction {next_num} deleted"
    }

    result2 = service.get(next_num)

    assert result2 == {
        "code": 200,
        "message": "ok",
        "data": {},
        "options": {}
    }
