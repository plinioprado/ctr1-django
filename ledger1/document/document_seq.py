"""
Show in a document as base (+)adds (-)subs = tot
Show in a transaction as debits or credits
The first seq, base, takes the dc of the document

Attributes:
    type: can be 'base', 'add', 'sub' or 'tot'
    text: account name ot a message to describe the seq
    acc: account number
    val: always positive amount
"""
from dataclasses import dataclass

@dataclass
class DocumentSeq:
    type: str
    text: str
    acc: str
    val: float

    def __post_init__(self) -> None:
        if self.type not in ["base", "add", "sub", "tot"]:
            raise ValueError("invalid doc_seq type")
        if (not isinstance(self.text, str)) or (not (3 <= len(self.type) <= 20)):
            raise ValueError("invalid doc_seq descr")
        if not isinstance(self.acc, str) or self.acc == "":
            raise ValueError("invalid doc_seq acc")
        if not isinstance(self.val, float) or self.val < 0:
            raise ValueError("invalid doc_seq val")

    def asdict(self) -> dict:
        return {
            "type": self.type,
            "text": self.text,
            "acc": self.acc,
            "val": self.val,
        }
