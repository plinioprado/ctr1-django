""" test of account crud """

# pylint: disable=missing-function-docstring

from ledger1.models.account1 import Account1
from ledger1.accounts1 import get, post, put, delete

def test_get():
    result: list = get(acc_from="1.1.1", acc_to="1.1.1")

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

    result: dict = post(Account1(
        num="9.9.9",
        name="test",
        dc=True))

    assert result == {
        "code": 200,
        "message": "account 9.9.9 created"
    }

    res2 = get(acc_from="9.9.9", acc_to="9.9.9")
    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test', 'dc': True}]
    }


def test_put():
    result: dict = put(Account1(
        num="9.9.9",
        name="test2",
        dc=True))

    assert result == {
        "code": 200,
        "message": "account 9.9.9 updated"
    }

    res2 = get(acc_from="9.9.9", acc_to="9.9.9")
    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test', 'dc': True}]
    }


def test_delete():
    result: str = delete("9.9.9")

    assert result == {
        "code": 200,
        "message": "account 9.9.9 deleted"
    }
