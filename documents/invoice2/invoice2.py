"""
Invoice2 is a simple invoice that can be stores in the tws double entry finance control

"""

from  dataclasses import dataclass, asdict
from documents.util import dateutil

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
    seller_name: str = ""
    buyer_name: str = ""
    descr: str = ""
    val_sale: float = 0
    val_gst: float = 0
    doc_type: str = "inv2"
    transaction_num = None
    seqs: list[Invoice2Seq] = []

    def __init__(self,  data):

        if (data["num"] is None):
            raise ValueError("missing invoice number")
        self.num = data["num"]

        self.set_dt(data["dt"])

        if (data["type"] is None):
            raise ValueError("missing invoice type")
        self.type = data["type"]

        if (data["seller_name"] is None and data["buyer_name"] is None):
            raise ValueError("missing invoice seller and buyer name" )
        self.seller_name = "" if data["seller_name"] is None else str(data["seller_name"])
        self.buyer_name = "" if data["buyer_name"] is None else str(data["buyer_name"])

        if data["descr"] is None:
            raise ValueError("missing invoice descr")
        self.descr = data["descr"]

        val_tot: float = 0
        self.seqs = []

        if data["val_sale"] is None:
            raise ValueError("missing invoice val_sale")
        self.seqs.append(Invoice2Seq(
            account=self._get_acc_from_type(),
            val=float(data["val_sale"]),
            dc=False,
            doc= {
                "type": "inv2",
                "num": data["num"]
            }))
        val_tot += float(data["val_sale"])
        self.val_sale = float(data["val_sale"])

        if data["val_gst"] is not None:
            self.seqs.append(Invoice2Seq(
                account="2.1.3",
                val=float(data["val_gst"]),
                dc=False,
                doc= {
                    "type": "",
                    "num": ""
                }))
            val_tot += float(data["val_gst"])
            self.val_gst = float(data["val_gst"])

        self.seqs.append(Invoice2Seq(
            account="1.1.3",
            val=val_tot,
            dc=True,
            doc= {
                "type": "",
                "num": ""
            }))

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
        if not isinstance(tra_num, int):
            raise ValueError(f"invalid transaction number {tra_num}")

        self.transaction_num = tra_num


    def asdict(self):
        return {
            "num": self.num,
            "dt": self.dt,
            "type": self.type,
            "seller_name": self.seller_name,
            "buyer_name": self.buyer_name,
            "descr": self.descr,
            "val_sale": self.seqs[0].val,
            "val_gst": self.seqs[1].val,
        }

    def assqlitetuple(self):
        """ returns the data stored in the table invoice1"""

        return (
            self.type,
            self.seller_name,
            self.buyer_name,
            self.descr,
            self.num,
        )

    def _get_acc_from_type(self):
        acc_raw = self.type.split(".")[1]
        acc_formated = f"{acc_raw[0]}.{acc_raw[1]}.{acc_raw[2]}"
        return acc_formated


    def get_transaction_dict(self):
        """ returns the data stored in the table transaction1_detail"""

        return {
            "num": self.transaction_num,
            "date" : self.dt,
            "descr": self.descr,
            "seqs": [asdict(s) for s in self.seqs]
        }


