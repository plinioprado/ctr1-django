""" Ledger transaction model """

import re
import datetime
from dataclasses import dataclass

@dataclass
class Transaction1SeqDoc:
    type: str
    num: str

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

    account: str
    val: float
    dc: bool
    doc: Transaction1SeqDoc

    def asdict(self):
        """ return the Transaction seq as a dict """

        return {
            "account": self.account,
            "val": self.val,
            "dc": self.dc,
            "doc": {
                "type": self.doc.type,
                "num": self.doc.num
            }
        }


@dataclass
class Transaction1:
    """
    Ledger transaction

    Attributes:
        num (int | "new" | None):
            if int: sequential number Id of the transaction,
            if None: Transaction being created so num was not yet assigned by the db
        date (str): transaction date in ISO format yyyy-mm-dd
        descr (str): description between 3 and 60 chars
        seqs (list[Transaction1Seq]): debits and credits of the transaction
    """

    num: int | None
    date: str
    descr: str
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

        if not isinstance(self.seqs, list):
            raise ValueError(f"invalid transaction seqs {self.seqs} (not list)")

        if len(self.seqs) < 2:
            raise ValueError(f"invalid transaction seqs {self.seqs} (less than 2)")

        netdc = 0
        for seq in self.seqs:

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
            "seqs": [seq.asdict() for seq in self.seqs]
        }
