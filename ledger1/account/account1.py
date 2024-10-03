""" Account model """

import re
from dataclasses import dataclass

@dataclass
class Account1:
    """  of a ledger1 account

    Attributes:
        num: str - logical sequence of numbers sepparaed by dots
        name: str - between 1 and ideally around 60 chars, but no limit
        dc: bool - True if Debit and False if Credit
    """

    num: str | None
    name: str
    dc: bool

    def __post_init__(self):
        """ individual validations """

        if not isinstance(self.num, str) or not re.match(r"^\d.\d.\d$", self.num):
            raise ValueError("invalid account number")

        if not isinstance(self.name, str) or not re.match(r"^.{3,90}$", self.num):
            raise ValueError("invalid account name")

        if self.dc not in [True, False]:
            raise ValueError("invalid account dc")


    def dict(self):
        """ converts class to dict """
        return {
            "num": self.num,
            "name": self.name,
            "dc": self.dc,
        }
