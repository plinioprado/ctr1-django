""" test of account crud """

# pylint: disable=missing-function-docstring

from ledger1.account.account_service import get, post, put, delete

def test_get():
    result: list = get(acc="111", acc_to="111")

    assert result == {
        "code": 200,
        "message": "ok",
        "data": [{
            'dc': True,
            'name': 'cash',
            'num': '1.1.1',
        }],
    }


def test_post():

    result: dict = post({
        "num": "9.9.9",
        "name": "test",
        "dc": True
    })

    assert result == {
        "code": 200,
        "message": "account 9.9.9 created"
    }

    res2 = get(acc="999", acc_to="999")
    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test', 'dc': True}]
    }


def test_put():
    result: dict = put({
        "num": "9.9.9",
        "name": "test2",
        "dc": True})

    assert result == {
        "code": 200,
        "message": "account 9.9.9 updated"
    }

    res2 = get(acc="999", acc_to="999")
    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test2', 'dc': True}]
    }


def test_delete():
    result: str = delete("999")

    assert result == {
        "code": 200,
        "message": "account 9.9.9 deleted"
    }
