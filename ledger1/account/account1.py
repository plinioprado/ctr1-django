""" Account model """

import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class Account1:
    """  of a ledger1 account

    Attributes:
        num: str - logical sequence of numbers sepparaed by dots
        name: str - between 1 and ideally around 60 chars, but no limit
        dc: bool - True if Debit and False if Credit
    """

    num: Optional[str] | None = None
    name: Optional[str] = None
    dc: Optional[bool] = None
    active: Optional[bool] = True
    doc_type: Optional[str] = ""
    doc_num: Optional[str] = ""


    def set_from_data(self, data) -> None:

        if isinstance(data["num"], str) and re.match(r"^\d.\d.\d$", data["num"]):
            self.num = data["num"]
        else:
            raise ValueError("invalid account number")

        if isinstance(data["name"], str) and re.match(r"^.{3,90}$", data["name"]):
            self.name = data["name"]
        else:
            raise ValueError("invalid account name")

        if data["dc"] in [True, False]:
            self.dc = data["dc"]
        else:
            raise ValueError("invalid account dc")

        if "active" in data.keys() and data["active"] is False:
            self.active = False
        else:
            self.active = True

        if "doc_type" in data.keys() and isinstance(data["doc_type"], str):
            self.doc_type = data["doc_type"]
        else:
            self.doc_type = ""

        if "doc_num" in data.keys() and isinstance(data["doc_num"], str):
            self.doc_num = data["doc_num"]
        else:
            self.doc_num= ""


    def dict(self) -> dict:
        """ converts class to dict """
        return {
            "num": self.num,
            "name": self.name,
            "dc": self.dc,
            "active": self.active,
            "doc_type": self.doc_type,
            "doc_num": self.doc_num,
        }
