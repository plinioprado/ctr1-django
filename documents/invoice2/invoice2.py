"""
Invoice2 is a simple invoice that can be stores in the tws double entry finance control

it contains
    Transaction
    TransactioDetail
    Complement
"""

class Invoice2:

    num: str = None
    dt: str = ""
    type: str = ""
    seller_name: str = ""
    buyer_name: str = ""
    descr: str = ""
    val_sale: float = 0
    val_gst: float = 0
    transaction_num = None

    def __init__(self,  data):

        if (data["num"] is None):
            raise ValueError("missing invoice number")
        self.num = data["num"]

        if (data["dt"] is None):
            raise ValueError("missing invoice data")
        self.dt = data["dt"]

        if (data["type"] is None):
            raise ValueError("missing invoice type")
        self.type = data["type"]

        if (data["seller_name"] is None and data["buyer_name"] is None):
            raise ValueError("missing invoice seller and buyer name" )
        self.seller_name = "" if data["seller_name"] is None else str(data["seller_name"])
        self.buyer_name = "" if data["buyer_name"] is None else str(data["buyer_name"])

        if (data["descr"] is None):
            raise ValueError("missing invoice descr")
        self.descr = data["descr"]

        if (data["val_sale"] is None):
            raise ValueError("missing invoice val_sale")
        self.val_sale = data["val_sale"]

        self.val_gst = data["val_gst"]

        if "transaction_num" in data.keys():
            self.transaction_num = data["transaction_num"]


    def asdict(self):
        return {
            "num": self.num,
            "dt": self.dt,
            "type": self.type,
            "seller_name": self.seller_name,
            "buyer_name": self.buyer_name,
            "descr": self.descr,
            "val_sale": self.val_sale,
            "val_gst": self.val_gst,
        }

    def assqlitetuple(self):
        return (
            self.dt,
            self.type,
            self.seller_name,
            self.buyer_name,
            self.descr,
            self.val_sale,
            self.val_gst,
            self.num,
        )

    def get_transaction_dict(self):
        seqs = [
                {
                    "account": "",
                    "val": self.val_sale,
                    "dc": False,
                    "doc": {
                        "type": "inv2",
                        "num": self.num
                    }
                },
                {
                    "account": "3.2.1",
                    "val": self.val_gst,
                    "dc": False,
                    "doc": {
                        "type": "",
                        "num": ""
                    }
                },
                {
                    "account": "1.1.3",
                    "val": (self.val_sale, + self.val_gst),
                    "dc": True,
                    "doc": {
                        "type": "",
                        "num": ""
                    }
                }
            ]

        return {
            "num": self.transaction_num,
            "date" : self.dt,
            "descr": self.descr,
            "seqs": seqs
        }
