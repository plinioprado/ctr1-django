""" Ledger transaction model """

import re
import datetime
from dataclasses import dataclass


@dataclass
class Transaction1Seq:
    """
    Debit or credit in a Ledger transaction

    Attributes:
        seq: int # sequential for that transaction
        account: str # logical seqience of numbers sepparaed by dots
        val: float # must be positive
        dc: bool # True if Debit and False if Credit
    """

    seq: int
    account: str
    val: float
    dc: bool


    def asdict(self):
        """ return the Transaction seq as a dict """

        return {
            "seq": self.seq,
            "account": self.account,
            "val": self.val,
            "dc": self.dc
        }


@dataclass
class Transaction1:
    """
    Ledger transaction

    Attributes:
        num (int | None): sequential number Id of the transaction,
            or None if it's being created so was not yet being assigned by the db
        date (str): transaction date in ISO format yyyy-mm-dd
        descr (str): description between 3 and 60 chars
        seqs (list[Transaction1Seq]): debits and credits of the transaction
    """

    num: int | None
    date: str
    descr: str
    doc_type: str
    doc_num: int
    seqs: list[Transaction1Seq]

    def __post_init__(self):

        if self.num is not None:
            if not isinstance(self.num, int) or self.num < 1:
                raise ValueError(f"invalid transaction num {self.num}")
            self.num = int(self.num)

        try:
            self.date = datetime.datetime.fromisoformat(self.date).isoformat()[0:10]
        except ValueError as err:
            raise ValueError(f"invalid transaction date {self.date}") from err

        if not isinstance(self.descr, str) or len(self.descr) < 3:
            raise ValueError(f"invalid transaction descr {self.descr}")

        if not isinstance(self.doc_type, str) or len(self.descr) < 1:
            raise ValueError(f"invalid transaction doc_type {self.doc_type}")

        if not isinstance(self.doc_num, int) or self.doc_num < 1:
            raise ValueError(f"invalid transaction doc_num {self.doc_num}")
        self.doc_num = int(self.doc_num)

        if not isinstance(self.seqs, list) or len(self.seqs) < 2:
            raise ValueError(f"invalid transaction seqs {self.seqs}")

        netdc = 0
        for k, seq in enumerate(self.seqs):
            if seq.seq != k + 1:
                raise ValueError(f"invalid transaction seq {seq.asdict()} (seq)")

            if not re.match(r"^\d.\d.\d$", seq.account):
                raise ValueError(f"invalid transaction seq {seq.asdict()} (acc)")

            if not isinstance(seq.val, float) or seq.val <= 0:
                raise ValueError(f"invalid transaction seq {seq.asdict()} (val)")

            if seq.dc not in [False,True]:
                raise ValueError(f"invalid transaction seq {seq.asdict()} (dc)")

            netdc += seq.val if seq.dc else -seq.val

        if netdc != 0:
            raise ValueError(f"invalid transaction seqs {self.seqs} (db and cr do not match)")


    def asdict(self) -> dict:
        """ return the Transaction as a dict """

        return {
            "num": self.num,
            "date" : self.date,
            "descr": self.descr,
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
            "seqs": [seq.asdict() for seq in self.seqs]
        }
