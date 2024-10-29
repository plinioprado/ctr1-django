from dataclasses import dataclass
#from ledger1.document.document_type import DocumentType

@dataclass
class Document1:
    num: str
    date: str
    val: float
    cpart_name: str

    def asdict(self) -> dict:
        return {
            "num": self.num,
            "date": self.date,
            "val": self.val,
            "cpart_name": self.cpart_name,
        }
