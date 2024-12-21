from dataclasses import dataclass

@dataclass
class Aux:

    # db
    table_name: str
    primary_key: str
    filter_field: str
    primary_key_form: str

    def __init__(self) -> None:
        pass

    def set_from_db(self, data) -> None:
        pass


    def set_from_request(self, data) -> None:
        pass


    def get_to_db(self) -> dict:
        return {}


    def get_to_response(self) -> dict:
        return {}


    def get_to_response_list(self) -> dict:
        return {}

    def get_to_response_new(self) -> dict:
        return {}


    @classmethod
    def get_db_format(cls) -> dict:
        return {}
