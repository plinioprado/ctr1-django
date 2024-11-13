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
    account_num: str = ""
    name: str = ""
    acc_num: str = ""
    seqs = []


    def set_from_db(self, data):
        doc_num: list[str] = data["doc_num"].split(".")
        self.institution_num: str = doc_num[0]
        self.institution_short_name: str = "RBC"
        self.transit_num: str = doc_num[1]
        self.account_num: str = doc_num[2]
        self.name: str = data["name"]
        self.acc_num = data["acc_num"]


    def set_seqs(self, doc_seqs: list[dict]):
        self.seqs = []
        for doc_seq in doc_seqs:
            self.seqs.append(BanstatSeq(
                dt=doc_seq["dt"],
                descr=doc_seq["descr"],
                db=doc_seq["db"],
                cr=doc_seq["cr"],
                bal=doc_seq["bal"]
            ))


    def toresult(self):
        seqs = [asdict(seq) for seq in self.seqs]
        return {
            "institution_num": self.institution_num,
            "transit_num": self.transit_num,
            "account_num": self.account_num,
            "name": self.name,
            "seqs": seqs
        }
