""" test Transaction model """

# pylint: disable=missing-function-docstring


from ledger1.transaction.transaction import Transaction, TransactionSeq, TransactionSeqDoc


def test_transaction_existent():

    tra = Transaction(
            num=1,
            date="2020-01-05",
            descr="test",
            seqs=[
                TransactionSeq(
                    account="1.1.1",
                    val=100.,
                    dc=True,
                    doc=TransactionSeqDoc(
                        type="bstat1",
                        num="1")
                ),
                TransactionSeq(
                    account="2.3.1",
                    val=100.,
                    dc=False,
                    doc=TransactionSeqDoc(
                        type="",
                        num="")
                )
            ]
    )

    assert tra.asdict() == {
        'num': 1,
        'date': "2020-01-05",
        'descr': "test",
        "seqs": [
            {
                "account": "1.1.1",
                "val": 100,
                "dc": True,
                "doc": {
                    "type": "bstat1",
                    "num": "1"
                }
            },
            {
                "account": "2.3.1",
                "val": 100,
                "dc": False,
                "doc": {
                    "type": "",
                    "num": "",
                }
            }
        ]
    }


def test_transaction_new():

    tra = Transaction(
            num=None,
            date="2020-01-05",
            descr="test",
            seqs=[
                TransactionSeq(
                    account="1.1.1",
                    val=100.,
                    dc=True,
                    doc=TransactionSeqDoc(
                        type="bstat1",
                        num="1")
                ),
                TransactionSeq(
                    account="2.3.1",
                    val=100.,
                    dc=False,
                    doc=TransactionSeqDoc(
                        type="",
                        num="")
                )
            ]
    )

    assert tra.asdict() == {
        'num': None,
        'date': "2020-01-05",
        'descr': "test",
        "seqs": [
            {
                "account": "1.1.1",
                "val": 100.,
                "dc": True,
                "doc": {
                    "type": "bstat1",
                    "num": "1",
                }
            },
            {
                "account": "2.3.1",
                "val": 100.,
                "dc": False,
                "doc": {
                    "type": "",
                    "num": "",
                }
            }
        ]
    }
