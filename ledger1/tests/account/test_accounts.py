""" test of account crud """

# pylint: disable=missing-function-docstring

from ledger1.account.account_service import get, post, put, delete

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_get():
    result: list = get(
        api_key=API_KEY,
        acc="111",
        acc_to="111")

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

    result: dict = post(
        api_key=API_KEY,
        data={
        "num": "9.9.9",
        "name": "test",
        "dc": True
    })

    assert result == {
        "code": 200,
        "message": "account 9.9.9 created"
    }

    res2 = get(
        api_key=API_KEY,
        acc="999",
        acc_to="999")

    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test', 'dc': True}]
    }


def test_put():
    result: dict = put(
        api_key=API_KEY,
        data={
        "num": "9.9.9",
        "name": "test2",
        "dc": True})

    assert result == {
        "code": 200,
        "message": "account 9.9.9 updated"
    }

    res2 = get(
        api_key=API_KEY,
        acc="999",
        acc_to="999")

    assert res2 == {
        "code": 200,
        "message": "ok",
        "data": [{'num': '9.9.9', 'name': 'test2', 'dc': True}]
    }


def test_delete():
    result: str = delete(
        api_key=API_KEY,
        acc_num="999")

    assert result == {
        "code": 200,
        "message": "account 9.9.9 deleted"
    }
