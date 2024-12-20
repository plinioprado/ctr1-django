from dataclasses import dataclass

@dataclass
class Setting:

    # fields
    key: str
    value: str

    # db
    table_name: str
    primary_key: str
    filter_field: dict

    def __init__(self):
        self.key = ""
        self.value = ""

        self.table_name = "setting"
        self.primary_key = "setting_key"
        self.filter_field = "setting_key"


    def set_from_db(self, data):
        self.key = data["setting_key"]
        self.value = data["setting_value"]


    def get_to_response(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_new(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_list(self):
        return {
            "key": self.key,
            "value": self.value
        }
