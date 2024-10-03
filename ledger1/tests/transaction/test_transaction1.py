""" test Transaction1 model """

# pylint: disable=missing-function-docstring


import datetime
from ledger1.transaction.transaction1 import Transaction1, Transaction1Seq


def test_transaction_existent():

    tra = Transaction1(
            num=1,
            date="2020-01-05",
            descr="test",
            doc_type="statement1",
            doc_num=1,
            seqs=[
                Transaction1Seq(
                    seq=1,
                    account="1.1.1",
                    val=100.,
                    dc=True
                ),
                Transaction1Seq(
                    seq=2,
                    account="2.3.1",
                    val=100.,
                    dc=False)
                ]
    )

    assert tra.asdict() == {
        'num': 1,
        'date': "2020-01-05",
        'descr': "test",
        "doc_type": "statement1",
        "doc_num": 1,
        "seqs": [
            {
                "seq": 1,
                "account": "1.1.1",
                "val": 100,
                "dc": True
            },
            {
                "seq": 2,
                "account": "2.3.1",
                "val": 100,
                "dc": False
            }
        ]
    }


def test_transaction_new():

    tra = Transaction1(
            num=None,
            date="2020-01-05",
            descr="test",
            doc_type="statement1",
            doc_num=1,
            seqs=[
                Transaction1Seq(
                    seq=1,
                    account="1.1.1",
                    val=100.,
                    dc=True
                ),
                Transaction1Seq(
                    seq=2,
                    account="2.3.1",
                    val=100.,
                    dc=False)
                ]
    )

    assert tra.asdict() == {
        'num': None,
        'date': "2020-01-05",
        'descr': "test",
        "doc_type": "statement1",
        "doc_num": 1,
        "seqs": [
            {
                "seq": 1,
                "account": "1.1.1",
                "val": 100,
                "dc": True
            },
            {
                "seq": 2,
                "account": "2.3.1",
                "val": 100,
                "dc": False
            }
        ]
    }
