from dataclasses import dataclass

@dataclass
class Setting:

    # fields
    key: str
    value: str

    # db
    table_name: str = "setting"
    primary_key: str = "setting_key"
    filter_field: str = "setting_key"
    primary_key_form: str = "key"


    def __init__(self):
        self.key = ""
        self.value = ""


    def set_from_db(self, data):
        self.key = data["setting_key"]
        self.value = data["setting_value"]


    def set_from_request(self, data):
        self.key = data["key"]
        self.value = data["value"]


    def get_to_db(self):
        return {
            "setting_key": self.key,
            "setting_value": self.value
        }


    def get_to_response(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_list(self):
        return {
            "key": self.key,
            "value": self.value
        }


    def get_to_response_new(self):
        return {
            "key": self.key,
            "value": self.value
        }


    @classmethod
    def get_db_format(cls):
        return {
            "setting_key": "str",
            "setting_value": "str",
        }
