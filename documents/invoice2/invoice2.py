"""
Invoice2 is a simple invoice that can be stored in the tws double entry finance control

"""

from  dataclasses import dataclass, asdict
from documents.util import dateutil
from documents.util import fileutil

@dataclass
class Invoice2Seq:
    account: str
    val: float
    dc: int
    doc: dict


class Invoice2:

    num: str = None
    dt: str = ""
    type: str = ""
    cpart_name: str = ""
    descr: str = ""
    doc_type: str = "inv2"
    doc_dc = True
    transaction_num = None
    seqs: list[Invoice2Seq] = []

    options: dict = {
        "seq_types": []
    }

    def __init__(self,  data):
        if data["num"] is None:
            raise ValueError("missing invoice number")
        self.num = data["num"]

        self.set_dt(data["dt"])

        if data["type"] is None:
            raise ValueError("missing invoice type")
        self.type = data["type"]

        if data["cpart_name"] is None:
            raise ValueError("missing invoice buyer name" )
        self.cpart_name = "" if data["cpart_name"] is None else str(data["cpart_name"])

        if data["descr"] is None:
            raise ValueError("missing invoice descr")
        self.descr = data["descr"]

        self.options["seq_types"] = fileutil.read_csv("./documents/dao/csv/document_seq_type.csv")
        doc_base_acc = data["seqs"][0]["account"]
        self.doc_dc = [tp for tp in self.options["seq_types"] if tp["acc"] == doc_base_acc][0]["doc_dc"] == 1

        seq_tot = 0
        self.seqs = []
        for key, seq in enumerate(data["seqs"]):
            seq_dc = self.get_dc_from_acc(seq["account"])
            val = float(seq["val"]) if key < len(data["seqs"]) - 1 else seq_tot
            self.seqs.append(Invoice2Seq(
                account=seq["account"],
                val=val,
                dc=seq_dc,
                doc= {
                    "type": self.doc_type if key == 0 else "",
                    "num": data["num"] if key == 0 else "",
                }))
            seq_tot += val

        # optional because will be set by the back-end based on self.num
        if "transaction_num" in data.keys():
            self.set_tra_num(data["transaction_num"])


    def set_dt(self, dt: str | int):
        if dt is None:
            raise ValueError("missing invoice data")

        try:
            if isinstance(dt, str):
                dt_stamp = dateutil.date_iso_to_timestamp(dt)
            else:
                dt_stamp = dt
            dt_iso = dateutil.date_timestamp_to_iso(dt_stamp)
            self.dt = dt_iso
        except ValueError as err:
            raise ValueError(f"invalid invoice data {dt}: {str(err)}") from err


    def set_tra_num(self, tra_num):
        """ some processes will need the tra_num in addition to the doc_num"""

        if not isinstance(tra_num, int):
            raise ValueError(f"invalid transaction number {tra_num}")

        self.transaction_num = tra_num


    def asdict(self):
        """ return a dict for a response """

        return {
            "num": self.num,
            "dt": self.dt,
            "type": self.type,
            "cpart_name": self.cpart_name,
            "descr": self.descr,
            "seqs": [asdict(seq) for seq in self.seqs],
        }

    def assqlitetuple(self):
        """ returns the data stored in the table invoice1"""

        return (
            self.type,
            self.cpart_name,
            self.descr,
            self.num,
        )

    def _get_acc_from_type(self):
        """ set tra.num based in doc.num """

        acc_raw = self.type.split(".")[1]
        acc_formated = f"{acc_raw[0]}.{acc_raw[1]}.{acc_raw[2]}"
        return acc_formated


    def get_transaction_dict(self):
        """ get the data for the table transaction1_detail"""

        return {
            "num": self.transaction_num,
            "date" : self.dt,
            "descr": self.descr,
            "seqs": [asdict(seq) for seq in self.seqs]
        }

    def get_dc_from_acc(self, acc: str) -> bool:

        dc = [tp for tp in self.options["seq_types"] if tp["acc"] == acc and bool(int(tp["doc_dc"]) == self.doc_dc)][0]["dc"] == "1"

        return dc


