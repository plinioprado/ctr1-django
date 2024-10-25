""" test Transaction1 model """

# pylint: disable=missing-function-docstring


from ledger1.transaction.transaction1 import Transaction1, Transaction1Seq, Transaction1SeqDoc


def test_transaction_existent():

    tra = Transaction1(
            num=1,
            date="2020-01-05",
            descr="test",
            seqs=[
                Transaction1Seq(
                    account="1.1.1",
                    val=100.,
                    dc=True,
                    doc=Transaction1SeqDoc(
                        type="bstat1",
                        num="1")
                ),
                Transaction1Seq(
                    account="2.3.1",
                    val=100.,
                    dc=False,
                    doc=Transaction1SeqDoc(
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

    tra = Transaction1(
            num=None,
            date="2020-01-05",
            descr="test",
            seqs=[
                Transaction1Seq(
                    account="1.1.1",
                    val=100.,
                    dc=True,
                    doc=Transaction1SeqDoc(
                        type="bstat1",
                        num="1")
                ),
                Transaction1Seq(
                    account="2.3.1",
                    val=100.,
                    dc=False,
                    doc=Transaction1SeqDoc(
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
