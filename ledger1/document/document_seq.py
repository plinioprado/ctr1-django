from dataclasses import dataclass, asdict

@dataclass
class DocumentSeq:
    type: str
    text: str
    acc: str
    val: float

    def asdict(self):
        return {
            "type": self.type,
            "text": self.text,
            "acc": self.acc,
            "val": self.val,
        }
