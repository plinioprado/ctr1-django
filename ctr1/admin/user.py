from dataclasses import dataclass
from datetime import datetime

from ctr1.admin.aux import Aux

@dataclass
class User(Aux):

    # db
    table_name = "user"
    primary_key = "id"
    filter_field = "name"
    primary_key_form = "id"

    def __init__(self) -> None:

        # fields
        self.id: str | None = None
        self.name: str = ""
        self.email: str = ""
        self.password: str = ""
        self.api_key: str = ""
        self.role: str = "user"
        self.expires: str | None = None
        self.active: bool = True


    def set_from_db(self, data: dict) -> None:
        self.id = str(data["id"]) if data["id"] is not None else None
        self.name = str(data["name"])
        self.email = str(data["email"])
        self.password = str(data["password"])
        self.api_key = str(data["api_key"])
        self.role = str(data["role"])
        self.active = bool(data["active"])
        self.expires = str(data["expires"])


    def set_from_request(self, data) -> None:
        self.id = str(data["id"]) if ("id" in data.keys() and data["id"] != "new") else None
        self.name = str(data["name"])
        self.email = str(data["email"])
        self.password = str(data["password"])
        self.api_key = datetime.now().strftime('%Y%m%d%1q2w3e4r5t6y7u8i9o0p')
        self.role = str(data["role"])
        self.active = bool(data["active"])
        self.expires = str(data["expires"])


    def get_to_db(self) -> dict:
        """ return to front-end all fields except password ans api_key """

        return {
            "id": self.id if self.id is not None else None,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "api_key": self.api_key,
            "role": self.role,
            "active": self.active,
            "expires": self.expires,
        }


    def get_to_response(self) -> dict:
        """ return to front-end all fields except password ans api_key """

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": "*" * 12,
            "role": self.role,
            "active": self.active,
            "expires": self.expires,
        }


    def get_to_response_list(self) -> dict:
        """ return to front-end all fields except password ans api_key """

        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "active": self.active,
        }


    def get_to_response_new(self):
        return {
            "id": "new",
            "name": "",
            "email": "",
            "password": "",
            "role": "user",
            "active": True,
            "expires": "",
        }


    @classmethod
    def get_db_format(cls) -> dict:
        return {
            "id": "int",
            "name": "str",
            "email": "str",
            "password": "str",
            "api_key": "str",
            "role": "str",
            "active": "bool",
            "expires": "date",
        }
