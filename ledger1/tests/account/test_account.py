""" test Account1 model """

# pylint: disable=missing-function-docstring

from ledger1.account.account1 import Account1


def test_account():

    acc = Account1()
    acc.set_from_data({
        "num": "9.9.9",
        "name": "test",
        "dc": False
    })

    assert acc.dict() == {
        'num': '9.9.9',
        'name': 'test',
        'dc': False,
        "active": True,
        "doc_type": "",
        "doc_num": ""
    }

def test_document():

    acc = Account1()
    acc.set_from_data({
        "num": "9.9.9",
        "name": "test",
        "dc": False,
        "active": False,
        "doc_type": "testtype",
        "doc_num": "123"
    })

    assert acc.dict() == {
        'num': '9.9.9',
        'name': 'test',
        'dc': False,
        "active": False,
        "doc_type": "testtype",
        "doc_num": "123"
    }
