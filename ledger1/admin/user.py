from dataclasses import dataclass

@dataclass
class User:
    id: int | str = "new"
    name: str = ""
    email: str = ""
    password: str = ""
    api_key: str = ""
    role: str = "user"
    entities: str = "example"
    entity: str = "example"
    active: bool = True

    def set_from_db(self, data):
        self.id = int(data["id"])
        self.name = str(data["name"])
        self.email = str(data["email"])
        self.password = str(data["password"])
        self.api_key = str(data["api_key"])
        self.role = str(data["role"])
        self.entities = str(data["entities"])
        self.entity = str(data["entity"])
        self.active = bool(data["active"])


    def get_to_response(self):
        """ return to front-end all fields except password ans api_key """

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "entities": self.entities,
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

