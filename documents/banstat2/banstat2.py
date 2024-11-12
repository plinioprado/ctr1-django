from dataclasses import dataclass, asdict

@dataclass
class BanstatSeq:
    dt: str = ""
    descr: str = ""
    cr: float = 0
    db: float = 0
    bal: float = 0


class Banstat2:
    institution_num: str = ""
    institution_short_name: str = ""
    transit_num: str = ""
    acc_num: str = ""
    descr: str = ""
    tra_acc: str = ""
    seqs = []

    def __init__(self):

        self.institution_num: str = "003"
        self.institution_short_name: str = "RBC"
        self.transit_num: str = "55555"
        self.acc_num: str = "7777777"
        self.descr: str = "rbc 55555-7777777 account"
        self.tra_acc_num = "1.1.2"

        self.seqs = []
        self.seqs.append(BanstatSeq(
            dt="2020-01-02",
            descr="opening balance",
            db=0,
            cr=0,
            bal=0
        ))
        self.seqs.append(BanstatSeq(
            dt="2020-01-02",
            descr="capital contribution",
            cr=10000,
            db=0,
            bal=10000
        ))

        self.seqs.append(BanstatSeq(
            dt="2020-01-05",
            descr="lawyer fees",
            cr=0,
            db=200,
            bal=9800
        ))
        self.seqs.append(BanstatSeq(
            dt="2020-01-21",
            descr="receiving from cedar store ltd",
            cr=0,
            db=11050,
            bal=10850,
        ))

    def toresult(self):
        seqs = [asdict(seq) for seq in self.seqs]
        return {
            "institution": f"{self.institution_num} - {self.institution_short_name}",
            "transit_num": self.transit_num,
            "acc_num": self.acc_num,
            "descr": self.descr,
            "seqs": seqs
        }
