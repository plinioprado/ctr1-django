""" Invoice1 model with structure and validations """

import datetime
import re

class Invoice1Model:

    def __init__(self, data: dict[str, str | int | float]) -> None:
        self._num: int = self.get_num(data["num"]) if "num" in data else 0
        self._value: float = self.get_value(data["value"])
        self._issue_date: datetime.date = self.get_issue_date(data["issue_date"])
        self._parts_seller_name: str = self.get_parts_seller_name(data["parts_seller_name"])
        self._parts_buyer_name: str = self.get_parts_buyer_name(data["parts_buyer_name"])
        self._status: str = self.get_status(data["status"]) if "status" in data else "open"


    def  dict(self) -> dict[str, str | int | float]:
        data: dict[str, str | int | float] = {
            "num": self.num,
            "value": self.value,
            "issue_date": self.issue_date,
            "parts_seller_name": self.parts_seller_name,
            "parts_buyer_name": self.parts_buyer_name,
            "status": self.status,
        }

        return data


    @property
    def num(self) -> int:
        return self._num

    def get_num(self, num: str | int | float) -> int:
        try:
            return int(num)
        except ValueError as err:
            raise ValueError("invalid invoice num") from err


    @property
    def value(self) -> float:
        return self._value

    def get_value(self, value: str | int | float) -> float:
        try:
            return float(value)
        except ValueError as err:
            raise ValueError("invalid invoice value") from err


    @property
    def issue_date(self) -> str:
        return datetime.date.isoformat(self._issue_date)

    def get_issue_date(self, issue_date: str | int | float) -> datetime.date:
        try:
            return datetime.date.fromisoformat(str(issue_date))
        except ValueError as err:
            raise ValueError("invalid invoice issue_date") from err


    @property
    def parts_seller_name(self) -> str:
        return self._parts_seller_name

    def get_parts_seller_name(self, parts_seller_name: str | int | float) -> str:
        try:
            if not re.match(r"^[A-Za-z0-9\s.]{3,30}$", str(parts_seller_name)):
                raise ValueError
            return str(parts_seller_name)
        except ValueError as err:
            raise ValueError("invalid invoice seller name") from err


    @property
    def parts_buyer_name(self) -> str:
        return self._parts_buyer_name

    def get_parts_buyer_name(self, parts_buyer_name: str | int | float) -> str:
        try:
            if not re.match(r"^[A-Za-z0-9\s.]{3,30}$", str(parts_buyer_name)):
                raise ValueError
            return str(parts_buyer_name)
        except ValueError as err:
            raise ValueError("invalid invoice buyer name (between 3 and 30 chars)") from err


    @property
    def status(self) -> str:
        return self._status

    def get_status(self, status: str | int | float) -> str:
        try:
            if status not in ["open", "cancelled", "paid"]:
                raise ValueError
            return str(status)
        except ValueError as err:
            raise ValueError("invalid invoice status") from err
