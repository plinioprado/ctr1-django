from dataclasses import dataclass

@dataclass
class Invoice2:

    num: int = None
    dt: str = ""
    type: str = ""
    seller_name: str = ""
    buyer_name: str = ""
    descr: str = ""
    val_sale: float = 0
    val_gst: float = 0

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
