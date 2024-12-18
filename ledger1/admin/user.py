from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:

    # fields
    id: int = None
    name: str = ""
    email: str = ""
    password: str = ""
    api_key: str = ""
    role: str = "user"
    entities: str = "example"
    entity: str = "example"
    active: bool = True

    # params
    table_name: str = "user"


    def set_from_db(self, data):
        self.id = int(data["id"]) if data["id"] is not None else None
        self.name = str(data["name"])
        self.email = str(data["email"])
        self.password = str(data["password"])
        self.api_key = str(data["api_key"])
        self.role = str(data["role"])
        self.entities = str(data["entities"])
        self.entity = str(data["entity"])
        self.active = bool(data["active"])


    def set_from_request(self, data):
        self.id = int(data["id"]) if ("id" in data.keys() and data["id"] is not None) else None
        self.name = str(data["name"])
        self.email = str(data["email"])
        self.password = str(data["password"])
        self.api_key = datetime.now().strftime('%Y%m%d%1q2w3e4r5t6y7u8i9o0p')
        self.role = str(data["role"])
        self.entities = str(data["entities"])
        self.entity = str(data["entity"])
        self.active = bool(data["active"])


    def get_to_db(self):
        """ return to front-end all fields except password ans api_key """

        return {
            "id": self.id if self.id is not None else None,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "api_key": self.api_key,
            "role": self.role,
            "entities": self.entities,
            "entity": self.entity,
            "active": self.active,
        }


    def get_to_response(self):
        """ return to front-end all fields except password ans api_key """

        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "password": "*" * 12,
            "role": self.role,
            "entities": self.entities,
            "entity": self.entity,
            "active": self.active,
        }


    def get_to_response_list(self):
        """ return to front-end all fields except password ans api_key """

        return {
            "id": str(self.id),
            "name": self.name,
            "role": self.role,
            "entity": self.entity,
            "active": self.active,
        }


    @classmethod
    def get_db_format(cls):
        return {
            "id": "int",
            "name": "str",
            "email": "str",
            "password": "str",
            "api_key": "str",
            "role": "str",
            "entities": "str",
            "entity": "str",
            "active": "bool",
        }
