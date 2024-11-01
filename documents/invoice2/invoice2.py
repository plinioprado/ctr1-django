from dataclasses import dataclass

@dataclass
class Invoice2:

    num: int = None
    date: str = ""
    type: list[tuple] = []
    seller_name: str = ""
    buyer_name: str = ""
    descr: str = ""
    val_sale: float = 0
    val_gst: float = 0


    def asdict(self):
        return {
            "num": self.num,
            "date": self.date,
            "type": self.type,
            "seller_name": self.seller_name,
            "buyer_name": self.buyer_name,
            "descr": self.descr,
            "val_sale": self.val_sale,
            "val_gst": self.val_gst,
        }
